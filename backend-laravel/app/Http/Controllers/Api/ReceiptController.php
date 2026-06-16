<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Receipt;
use Illuminate\Http\Request;

class ReceiptController extends Controller
{
    public function index()
    {
        $receipts = Receipt::orderBy('created_at', 'desc')->get();
        return response()->json([
            'status' => 'success',
            'data' => $receipts
        ]);
    }

    public function upload(Request $request)
    {
        $request->validate([
            'file' => 'required|image|mimes:jpg,jpeg,png,webp|max:10240'
        ]);

        $file = $request->file('file');
        $filename = $file->getClientOriginalName();
        $path = $file->store('receipts', 'public');

        // TODO: Panggil Gemini Vision API untuk OCR
        // $ocrResult = app(GeminiService::class)->analyzeReceipt($file);

        return response()->json([
            'message' => 'Receipt uploaded for OCR processing',
            'filename' => $filename,
            'path' => $path
        ]);
    }
}
