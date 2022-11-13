from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Post, Author


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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "listing/new.html"
    fields = (
        "title",
        "content",
    )

    def form_valid(self, form):
        post = form.save(commit=False)
        init_author = Author.objects.get(author=self.request.user)
        post.author = init_author
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "listing/delete.html"
    success_url = reverse_lazy("post_list")
    permission_required = ('listings.delete_post',)

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = "listing/edit.html"
    permission_required = ('listing.change_post',)

    fields = (
        "title",
        "content",
    )

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
