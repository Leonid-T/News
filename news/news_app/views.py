from django.views import View
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, permissions

from .models import Post
from .serializers import PostSerializer
from .forms import SigninForm, SignupForm


class IndexView(View):
    """
    View of news list
    """
    paginate_by = 6
    template_name = 'index.html'

    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # dynamic loading of news
            posts = Post.objects.order_by('-added_at')

            paginator = Paginator(posts, self.paginate_by)
            page_number = request.GET.get('page')
            try:
                page_obj = paginator.page(page_number)
            except (EmptyPage, PageNotAnInteger):
                # if news posts run out or uncorrect page parameter
                return JsonResponse({'status': 404})

            return render(request, 'block/post.html', context={
                'news_list': page_obj,
            })

        return render(request, self.template_name)


class DetailView(View):
    """
    News post detail view
    """
    template_name = 'detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.views_counter()

        # checking if the user has liked
        user = request.user
        is_like = False
        if user.is_authenticated:
            is_like = post.is_like(user)

        return render(request, self.template_name, context={
            'post': post,
            'is_like': 'active' if is_like else ''
        })


class TagView(View):
    """
    View of news list with tag
    """
    template_name = 'tag.html'
    paginate_by = 6

    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        common_tags = Post.tags.most_common()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # dynamic loading of news
            posts = Post.objects.filter(tags=tag).order_by('-added_at')

            paginator = Paginator(posts, self.paginate_by)
            page_number = request.GET.get('page')
            try:
                page_obj = paginator.page(page_number)
            except (EmptyPage, PageNotAnInteger):
                # if news posts run out or uncorrect page parameter
                return JsonResponse({'status': 404})

            return render(request, 'block/post.html', context={
                'news_list': page_obj,
            })

        return render(request, self.template_name, context={
            'tag': tag,
            'common_tags': common_tags[:10]
        })


class StatisticsView(View):
    """
    View of news list with statistic
    """
    paginate_by = 10
    template_name = 'statistics.html'

    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # dynamic loading of news
            posts = Post.objects.order_by('-views_count', '-added_at')

            paginator = Paginator(posts, self.paginate_by)
            page_number = request.GET.get('page')
            try:
                page_obj = paginator.page(page_number)
            except (EmptyPage, PageNotAnInteger):
                # if news posts run out or uncorrect page parameter
                return JsonResponse({'status': 404})

            return render(request, 'block/post_statistic.html', context={
                'news_list': page_obj,
            })

        return render(request, self.template_name)


class PostViewSet(viewsets.ModelViewSet):
    """
    REST API for post table
    Without authorization!!!
    """
    search_fields = ['content', 'title']
    serializer_class = PostSerializer
    queryset = Post.objects.order_by('-added_at')
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]


class SignupView(View):
    """
    Registration view
    """
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return JsonResponse({'url': reverse('news:index')}, status=200)

        return JsonResponse({'error': form.errors}, status=400)


class SigninView(View):
    """
    Authorization view
    """
    def get(self, request):
        form = SigninForm()
        return render(request, 'signin.html', {'form': form})

    def post(self, request):
        form = SigninForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return JsonResponse({'url': reverse('news:index')}, status=200)

        form.add_error('password', 'Неправильное имя пользователя или пароль')
        return JsonResponse({'error': form.errors}, status=400)


class VoteView(View):
    """
    Setting or unsetting like
    """
    def post(self, request, pk):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Is not authenticated'}, status=400)

        post = get_object_or_404(Post, pk=pk)
        result = post.set_like(user)
        return JsonResponse({
            'id': post.id,
            'result': result,
            'rating': post.like_count(),
        }, status=200)
