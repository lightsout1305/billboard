from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.sites.models import Site
from django.db.models import Q

from .models import Post, Author, Comment
from .forms import CommentForm, PostForm


class PostListView(ListView):
    model = Post
    template_name = 'listing/main.html'
    context_object_name = 'listings'
    paginate_by = 10
    ordering = 'register_date'


class PostDetailView(DetailView, FormView):
    model = Post
    template_name = 'listing/detail.html'
    context_object_name = 'one_post'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        post = self.get_object()
        return reverse("post_detail", kwargs={"pk": post.pk})

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.comment_post = self.object
        comment.comment_author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.get_current().domain
        context['comment'] = Comment
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "listing/new.html"
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        init_author = Author.objects.get(author=self.request.user)
        post.author = init_author
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "listing/delete.html"
    success_url = reverse_lazy("post_list")
    permission_required = ('listings.delete_post',)

    def test_func(self):
        obj = self.get_object()
        return obj.author.author == self.request.user


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "listing/edit.html"
    permission_required = ('listings.change_post',)

    fields = (
        "title",
        "content",
    )

    def form_valid(self, form):
        post = form.save(commit=False)
        init_author = Author.objects.get(author=self.request.user)
        post.author = init_author
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.author.author == self.request.user


class SearchResultsListView(ListView):
    model = Post
    context_object_name = 'listings_list'
    template_name = 'listing/search_results.html'
    paginate_by = 10
    queryset = Post.objects.all().order_by('id')

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Post.objects.filter(
            Q(title__icontains=query) | Q(author__author__username__contains=query)
        )


