from .models import Post
from django.views.generic import ListView, DetailView


class PostListView(ListView):
    model = Post
    template_name = 'listing/main.html'
    context_object_name = 'listings'
    paginate_by = 10
    queryset = Post.objects.all().order_by('id')


class PostDetailView(DetailView):
    model = Post
    template_name = 'listing/detail.html'
    context_object_name = 'one_post'


# Create your views here.
