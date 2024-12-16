from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField("Название категории", max_length=100)
    slug = models.SlugField("Слаг", unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField("Название тега", max_length=100)
    slug = models.SlugField("Слаг", unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name

class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('pending', 'На модерации'),
        ('published', 'Опубликован'),
    ]


    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField("Содержание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="news", verbose_name="Категория", default=1)
    tags = models.ManyToManyField(Tag, blank=True, related_name="news", verbose_name="Теги")
    image = models.ImageField("Изображение", upload_to='news_images/')
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор", null=True, blank=True)
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def short_content(self):
        return f"{self.content[:100]}..." if len(self.content) > 100 else self.content