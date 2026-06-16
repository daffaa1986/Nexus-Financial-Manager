<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('receipts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->default(1)->constrained('users')->onDelete('cascade');
            $table->string('store_name')->nullable();
            $table->decimal('total_amount', 15, 2)->default(0);
            $table->date('date')->nullable();
            $table->json('items')->nullable();
            $table->text('raw_ocr_text')->nullable();
            $table->string('image_path')->nullable();
            $table->string('category')->nullable();
            $table->timestamps();

            $table->index('user_id');
            $table->index('store_name');
            $table->index('date');
        });
    }

    public function down()
    {
        Schema::dropIfExists('receipts');
    }
};
