<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('budgets', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->default(1)->constrained('users')->onDelete('cascade');
            $table->string('category');
            $table->decimal('monthly_limit', 15, 2);
            $table->integer('month');
            $table->integer('year');
            $table->timestamps();

            $table->unique(['user_id', 'category', 'month', 'year']);
            $table->index(['month', 'year']);
        });
    }

    public function down()
    {
        Schema::dropIfExists('budgets');
    }
};
