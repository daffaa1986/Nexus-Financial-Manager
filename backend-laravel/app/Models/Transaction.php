<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Transaction extends Model
{
    protected $fillable = [
        'user_id', 'date', 'label', 'amount', 'category',
        'type', 'source', 'source_file', 'month', 'year', 'bank'
    ];

    protected $casts = [
        'amount' => 'float',
        'date' => 'date',
        'month' => 'integer',
        'year' => 'integer',
    ];

    public function scopeIncome($query)
    {
        return $query->where('type', 'CR');
    }

    public function scopeExpense($query)
    {
        return $query->where('type', 'DB');
    }

    public function scopeByMonth($query, $bulan, $tahun)
    {
        return $query->where('month', $bulan)->where('year', $tahun);
    }

    public function scopeByCategory($query, $category)
    {
        return $query->where('category', $category);
    }
}
