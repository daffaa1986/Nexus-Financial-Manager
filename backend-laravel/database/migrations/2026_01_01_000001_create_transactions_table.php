<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('transactions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->default(1)->constrained('users')->onDelete('cascade');
            $table->date('date')->nullable();
            $table->string('label')->nullable();
            $table->decimal('amount', 15, 2)->default(0);
            $table->string('category')->nullable();
            $table->enum('type', ['DB', 'CR'])->default('DB');
            $table->enum('source', ['mutation', 'receipt'])->default('mutation');
            $table->string('source_file')->nullable();
            $table->integer('month')->nullable();
            $table->integer('year')->nullable();
            $table->string('bank')->default('BCA');
            $table->timestamps();

            $table->index(['month', 'year']);
            $table->index('user_id');
            $table->index('category');
            $table->index('date');
        });
    }

    public function down()
    {
        Schema::dropIfExists('transactions');
    }
};
