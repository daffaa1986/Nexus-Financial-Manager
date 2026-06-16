<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Transaction;
use App\Models\Receipt;
use Illuminate\Http\Request;

class InsightController extends Controller
{
    public function index(Request $request)
    {
        $bulan = $request->query('bulan', date('n'));
        $tahun = $request->query('tahun', date('Y'));

        $transactions = Transaction::byMonth($bulan, $tahun)->get();
        $receipts = Receipt::all();

        $totalIncome = $transactions->where('type', 'CR')->sum('amount');
        $totalExpense = $transactions->where('type', 'DB')->sum('amount');
        $balance = $totalIncome - $totalExpense;
        $savingsRate = $totalIncome > 0 ? round(($balance / $totalIncome) * 100, 1) : 0;

        $byCategory = $transactions->where('type', 'DB')
            ->groupBy('category')
            ->map(function ($items) {
                return [
                    'total' => $items->sum('amount'),
                    'count' => $items->count(),
                    'avg' => round($items->avg('amount')),
                ];
            });

        $insights = $this->generateInsights($transactions, $receipts);

        return response()->json([
            'status' => 'success',
            'data' => [
                'stats' => [
                    'income' => $totalIncome,
                    'expense' => $totalExpense,
                    'balance' => $balance,
                    'savings_rate' => $savingsRate,
                    'by_category' => $byCategory,
                    'trx_count' => $transactions->count(),
                    'receipt_count' => $receipts->count(),
                ],
                'insights' => $insights,
                'summary' => $this->buildSummary($totalIncome, $totalExpense, $balance, $savingsRate, count($insights)),
            ]
        ]);
    }

    public function generate(Request $request)
    {
        return response()->json([
            'status' => 'success',
            'data' => [
                'insights' => [] // TODO: Call Gemini AI API
            ]
        ]);
    }

    public function comparison(Request $request)
    {
        $bulan = (int) $request->query('bulan', date('n'));
        $tahun = (int) $request->query('tahun', date('Y'));

        $bulanLalu = $bulan - 1;
        $tahunLalu = $tahun;
        if ($bulanLalu === 0) { $bulanLalu = 12; $tahunLalu--; }

        $curr = Transaction::byMonth($bulan, $tahun)->get();
        $prev = Transaction::byMonth($bulanLalu, $tahunLalu)->get();

        return response()->json([
            'status' => 'success',
            'data' => [
                'current' => [
                    'income' => $curr->where('type', 'CR')->sum('amount'),
                    'expense' => $curr->where('type', 'DB')->sum('amount'),
                ],
                'previous' => [
                    'income' => $prev->where('type', 'CR')->sum('amount'),
                    'expense' => $prev->where('type', 'DB')->sum('amount'),
                ]
            ]
        ]);
    }

    public function summary(Request $request)
    {
        $bulan = (int) $request->query('bulan', date('n'));
        $tahun = (int) $request->query('tahun', date('Y'));

        $transactions = Transaction::byMonth($bulan, $tahun)->get();
        $income = $transactions->where('type', 'CR')->sum('amount');
        $expense = $transactions->where('type', 'DB')->sum('amount');
        $byCategory = $transactions->where('type', 'DB')->groupBy('category')
            ->map(fn($items) => $items->sum('amount'));

        return response()->json([
            'status' => 'success',
            'data' => [
                'income' => $income,
                'expense' => $expense,
                'balance' => $income - $expense,
                'savings_rate' => $income > 0 ? round(($income - $expense) / $income * 100, 1) : 0,
                'kategori' => $byCategory->map(fn($total, $cat) => ['category' => $cat, 'total' => $total])->values(),
            ]
        ]);
    }

    public function daily(Request $request)
    {
        $bulan = (int) $request->query('bulan', date('n'));
        $tahun = (int) $request->query('tahun', date('Y'));

        $transactions = Transaction::byMonth($bulan, $tahun)->get();
        $daily = $transactions->groupBy('date')->map(function ($items) {
            return [
                'income' => $items->where('type', 'CR')->sum('amount'),
                'expense' => $items->where('type', 'DB')->sum('amount'),
                'count' => $items->count(),
            ];
        });

        return response()->json([
            'status' => 'success',
            'data' => $daily
        ]);
    }

    private function generateInsights($transactions, $receipts)
    {
        $insights = [];

        // Detect bocor (small frequent expenses)
        $smallByLabel = [];
        foreach ($transactions->where('type', 'DB') as $t) {
            if ($t->amount < 50000) {
                $label = preg_replace('/\d+/', '', $t->label);
                $label = substr($label, 0, 30);
                if (!isset($smallByLabel[$label])) {
                    $smallByLabel[$label] = ['total' => 0, 'count' => 0];
                }
                $smallByLabel[$label]['total'] += $t->amount;
                $smallByLabel[$label]['count']++;
            }
        }

        foreach ($smallByLabel as $label => $data) {
            if ($data['count'] >= 3 && $data['total'] >= 50000) {
                $insights[] = [
                    'type' => 'bocor',
                    'title' => "Pengeluaran kecil tapi sering: {$label}",
                    'description' => "{$data['count']}x transaksi = Rp " . number_format($data['total'], 0, ',', '.') . "/bulan",
                    'severity' => $data['total'] >= 200000 ? 'high' : 'medium',
                    'amount' => $data['total'],
                ];
            }
        }

        // Detect boros (biggest category)
        $totalExpense = $transactions->where('type', 'DB')->sum('amount');
        $byCategory = $transactions->where('type', 'DB')->groupBy('category')
            ->map(fn($items) => ['total' => $items->sum('amount')])
            ->sortByDesc('total');

        if ($byCategory->isNotEmpty() && $totalExpense > 0) {
            $topCat = $byCategory->keys()->first();
            $topTotal = $byCategory->first()['total'];
            $persen = round(($topTotal / $totalExpense) * 100, 1);
            if ($persen > 40) {
                $insights[] = [
                    'type' => 'boros',
                    'title' => "Pengeluaran terbesar: {$topCat}",
                    'description' => "{$persen}% dari total pengeluaran (Rp " . number_format($topTotal, 0, ',', '.') . ")",
                    'severity' => $persen > 50 ? 'high' : 'medium',
                    'amount' => $topTotal,
                ];
            }
        }

        return $insights;
    }

    private function buildSummary($income, $expense, $balance, $savingsRate, $insightCount)
    {
        $lines = [];
        $lines[] = "Total Pemasukan: Rp " . number_format($income, 0, ',', '.');
        $lines[] = "Total Pengeluaran: Rp " . number_format($expense, 0, ',', '.');
        $lines[] = "Saldo Bersih: Rp " . number_format($balance, 0, ',', '.');
        $lines[] = "Rasio Tabungan: {$savingsRate}%";

        if ($insightCount > 0) {
            $lines[] = "\nAda {$insightCount} masalah yang perlu diperhatikan!";
        } else {
            $lines[] = "\nKeuangan dalam kondisi cukup baik.";
        }

        return implode("\n", $lines);
    }
}
