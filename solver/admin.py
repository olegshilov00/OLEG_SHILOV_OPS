from django.contrib import admin
from .models import QuadraticSolution


@admin.register(QuadraticSolution)
class QuadraticSolutionAdmin(admin.ModelAdmin):
    list_display = ('a', 'b', 'c', 'user_solution', 'correct_solution', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at')
    search_fields = ('a', 'b', 'c')