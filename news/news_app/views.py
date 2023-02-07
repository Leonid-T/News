from django.views import generic, View
from django.shortcuts import get_object_or_404, render
from taggit.models import Tag
from django.core.paginator import Paginator

from .models import Post


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'news_list'
    paginate_by = 5
    queryset = Post.objects.order_by('-added_at')


class DetailView(generic.DetailView):
    model = Post
    template_name = 'detail.html'
    queryset = Post.objects.all()


class TagView(View):
    template_name = 'tag.html'
    paginate_by = 5

    def get(self, request, tag_slug):
        tag = get_object_or_404(Tag, slug=tag_slug)
        common_tags = Post.tags.most_common()

        posts = Post.objects.filter(tags=tag).order_by('-added_at')
        paginator = Paginator(posts, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, context={
            'tag': tag,
            'news_list': page_obj,
            'common_tags': common_tags
        })
