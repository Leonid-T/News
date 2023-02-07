from django.views import generic, View
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
    paginate_by = 6
    template_name = 'index.html'

    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            posts = Post.objects.order_by('-added_at')

            paginator = Paginator(posts, self.paginate_by)
            page_number = request.GET.get('page')
            try:
                page_obj = paginator.page(page_number)
            except (EmptyPage, PageNotAnInteger):
                return JsonResponse({'status': 404})

            return render(request, 'block/post.html', context={
                'news_list': page_obj,
            })

        return render(request, self.template_name)


class DetailView(generic.DetailView):
    model = Post
    template_name = 'detail.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Post, pk=pk)
        obj.views_counter()
        return obj


class TagView(View):
    template_name = 'tag.html'
    paginate_by = 6

    def get(self, request, tag_slug):
        tag = get_object_or_404(Tag, slug=tag_slug)
        common_tags = Post.tags.most_common()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            posts = Post.objects.filter(tags=tag).order_by('-added_at')

            paginator = Paginator(posts, self.paginate_by)
            page_number = request.GET.get('page')
            try:
                page_obj = paginator.page(page_number)
            except (EmptyPage, PageNotAnInteger):
                return JsonResponse({'status': 404})

            return render(request, 'block/post.html', context={
                'news_list': page_obj,
            })

        return render(request, self.template_name, context={
            'tag': tag,
            'common_tags': common_tags
        })


class StatisticsView(View):
    paginate_by = 8
    template_name = 'statistics.html'

    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            posts = Post.objects.order_by('-views_count', '-added_at')

            paginator = Paginator(posts, self.paginate_by)
            page_number = request.GET.get('page')
            try:
                page_obj = paginator.page(page_number)
            except (EmptyPage, PageNotAnInteger):
                return JsonResponse({'status': 404})

            return render(request, 'block/post_statistic.html', context={
                'news_list': page_obj,
            })

        return render(request, self.template_name)


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'title']
    serializer_class = PostSerializer
    queryset = Post.objects.order_by('-added_at')
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]


class SignupView(View):
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
    def get(self, request):
        form = SigninForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = SigninForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return JsonResponse({'url': reverse('news:index')}, status=200)
        form.add_error('password', 'Неправильное имя пользователя или пароль')
        return JsonResponse({'error': form.errors}, status=400)
