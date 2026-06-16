<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Receipt extends Model
{
    protected $fillable = [
        'user_id', 'store_name', 'total_amount', 'date',
        'items', 'raw_ocr_text', 'image_path', 'category'
    ];

    protected $casts = [
        'total_amount' => 'float',
        'items' => 'array',
        'date' => 'date',
    ];

    public function getItemCountAttribute()
    {
        $items = $this->items ? json_decode($this->items, true) : [];
        return count($items);
    }
}
