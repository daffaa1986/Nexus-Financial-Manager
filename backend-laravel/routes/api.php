<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\TransactionController;
use App\Http\Controllers\Api\InsightController;
use App\Http\Controllers\Api\ReceiptController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Nexus Finance API - Mirroring FastAPI endpoints in Laravel
|
*/

// Transactions
Route::get('/transactions', [TransactionController::class, 'index']);
Route::get('/transactions/month/{bulan}/{tahun}', [TransactionController::class, 'byMonth']);
Route::post('/upload', [TransactionController::class, 'upload']);
Route::post('/upload-receipt', [ReceiptController::class, 'upload']);

// Receipts
Route::get('/receipts', [ReceiptController::class, 'index']);

// AI Insights
Route::get('/insights', [InsightController::class, 'index']);
Route::get('/insights/generate', [InsightController::class, 'generate']);
Route::get('/comparison', [InsightController::class, 'comparison']);
Route::get('/summary', [InsightController::class, 'summary']);
Route::get('/analytics/daily', [InsightController::class, 'daily']);

// Goals & Budgets
Route::get('/goals', [TransactionController::class, 'goals']);
Route::post('/goals', [TransactionController::class, 'createGoal']);
Route::get('/budgets', [TransactionController::class, 'budgets']);
Route::post('/budgets', [TransactionController::class, 'setBudget']);
