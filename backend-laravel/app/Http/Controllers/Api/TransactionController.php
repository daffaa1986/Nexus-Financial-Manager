<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Transaction;
use App\Models\Receipt;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class TransactionController extends Controller
{
    public function index()
    {
        $transactions = Transaction::orderBy('date', 'desc')->get();
        return response()->json([
            'status' => 'success',
            'data' => $transactions
        ]);
    }

    public function byMonth($bulan, $tahun)
    {
        $transactions = Transaction::byMonth($bulan, $tahun)
            ->orderBy('date', 'asc')
            ->get();
        return response()->json([
            'status' => 'success',
            'data' => $transactions,
            'month' => (int) $bulan,
            'year' => (int) $tahun
        ]);
    }

    public function upload(Request $request)
    {
        $request->validate([
            'file' => 'required|file|mimes:pdf,jpg,jpeg,png,webp|max:10240'
        ]);

        $file = $request->file('file');
        $filename = $file->getClientOriginalName();
        $ext = strtolower($file->getClientOriginalExtension());

        if (in_array($ext, ['jpg', 'jpeg', 'png', 'webp'])) {
            // OCR Receipt - implementasi panggil Gemini API
            $path = $file->store('receipts', 'public');
            return response()->json([
                'message' => 'Receipt uploaded for OCR processing',
                'filename' => $filename,
                'path' => $path
            ]);
        }

        // Process PDF mutation
        $path = $file->store('mutations', 'public');

        // TODO: Panggil AI Engine (Python microservice or PHP Gemini SDK)
        return response()->json([
            'message' => 'Mutation file uploaded, processing in background',
            'filename' => $filename
        ]);
    }

    public function goals()
    {
        return response()->json([
            'status' => 'success',
            'data' => [] // TODO: Implement goals query
        ]);
    }

    public function createGoal(Request $request)
    {
        $request->validate([
            'name' => 'required|string',
            'target_amount' => 'required|numeric',
            'deadline' => 'required|date',
            'category' => 'string'
        ]);

        // TODO: Save goal to database

        return response()->json([
            'status' => 'success',
            'message' => 'Goal created successfully'
        ]);
    }

    public function budgets()
    {
        return response()->json([
            'status' => 'success',
            'data' => [] // TODO: Implement budgets query
        ]);
    }

    public function setBudget(Request $request)
    {
        $request->validate([
            'category' => 'required|string',
            'monthly_limit' => 'required|numeric',
            'bulan' => 'integer',
            'tahun' => 'integer'
        ]);

        // TODO: Save budget to database

        return response()->json([
            'status' => 'success',
            'message' => 'Budget saved successfully'
        ]);
    }
}
