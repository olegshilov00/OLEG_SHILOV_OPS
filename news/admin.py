from django.contrib import admin
from .models import News, Category, Tag
import string

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_at', 'author')
    list_filter = ('status', 'category', 'tags', 'created_at')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Если это новый объект
            obj.status = 'published'  # Автоматически публикуем
        obj.save()

    def punctuation_count(self, obj):
        """Подсчитывает количество знаков препинания в тексте новости."""
        punctuation_marks = string.punctuation
        return sum(1 for char in obj.content if char in punctuation_marks)

    punctuation_count.short_description = 'Количество знаков препинания'

    class Media:
        css = {
            'all': ('css/admin_custom.css',),
        }
