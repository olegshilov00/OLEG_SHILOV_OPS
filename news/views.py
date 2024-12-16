from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import News, Category, Tag
from .forms import NewsForm

class NewsListView(View):
    @method_decorator(cache_page(60 * 1))
    def get(self, request):
        """
        GET method for NewsListView.

        This method renders the news_list.html template with a list of
        published news items, categories, and tags. The news items are
        paginated with 4 items per page.
        """
        news_items = News.objects.filter(status='published')
        categories = Category.objects.all()
        tags = Tag.objects.all()
        paginator = Paginator(news_items, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'news/news_list.html', {
            'page_obj': page_obj,
            'categories': categories,
            'tags': tags
        })

class NewsDetailView(View):
    @method_decorator(cache_page(60 * 1))
    def get(self, request, pk):
        """
        GET method for NewsDetailView.

        This method renders the news_detail.html template with a
        specific news item based on the given primary key. The news
        item must be published. The method is cached for 1 minute.
        """
        news = get_object_or_404(News, pk=pk)
        return render(request, 'news/news_detail.html', {'news': news})

class NewsByCategoryView(View):
    @method_decorator(cache_page(60 * 1))
    def get(self, request, slug):
        """
        GET method for NewsByCategoryView.

        This method renders the news_by_category.html template with a list of
        published news items in the given category. The method is cached for 1
        minute.
        """
        category = get_object_or_404(Category, slug=slug)
        news_items = category.news.filter(status='published')
        return render(request, 'news/news_by_category.html', {'category': category, 'news_items': news_items})

class NewsByTagView(View):
    @method_decorator(cache_page(60 * 1))
    def get(self, request, slug):
        
        """
        GET method for NewsByTagView.

        This method renders the news_by_tag.html template with a list of
        published news items in the given tag. The method is cached for 1
        minute.
        """
        tag = get_object_or_404(Tag, slug=slug)
        news_items = tag.news.filter(status='published')
        return render(request, 'news/news_by_tag.html', {'tag': tag, 'news_items': news_items})

class CreatePostView(View):
    @method_decorator(login_required)
    def get(self, request):
        """
        GET method for CreatePostView.

        This method renders the create_post.html template with an empty NewsForm.
        The method is decorated with login_required to ensure that only
        authenticated users can create posts.
        """
        form = NewsForm()
        return render(request, 'news/create_post.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        """
        POST method for CreatePostView.

        This method processes the form data sent with the POST request.
        If the form is valid, it creates a new News object with the given
        data, sets the author to the current user, and sets the status to
        'pending'. The method then redirects to the news list page.
        If the form is not valid, it renders the create_post.html template
        with the invalid form.
        """
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'pending'
            post.save()
            form.save_m2m()
            return redirect('news_list')
        return render(request, 'news/create_post.html', {'form': form})
