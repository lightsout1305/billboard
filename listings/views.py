from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy, reverse
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.db.models import Q

from .models import Post, Author, Comment, Category, CategorySubs
from .forms import CommentForm, PostForm
from billboard_project.settings import SERVER_EMAIL


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


class CategoryDetail(PermissionRequiredMixin, ListView):
    model = Category
    context_object_name = 'category_detail'
    template_name = 'listing/main.html'
    permission_required = ('news_project.view_category',)

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('id')
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['category_post'] = Post.objects.filter(postcategory=id)
        context['name'] = Category.objects.filter(id=id)
        is_subscribed = CategorySubs.objects.filter(cat_sub_category_id=id, cat_sub_user=user).exists()
        context['is_subscribed'] = is_subscribed
        return context


@login_required
def add_subscription(request, pk):
    user = request.user
    catgr = Category.objects.get(id=pk)
    is_subscribed = CategorySubs.objects.filter(cat_sub_user_id=user.id, cat_sub_category_id=catgr.id)

    if request.method == 'POST':
        if not is_subscribed:
            CategorySubs.objects.create(cat_sub_user_id=user.id, cat_sub_category_id=catgr.id)
            catgr_repr = f'{catgr}'
            email = user.email
            msg = EmailMultiAlternatives(
                subject=f'Subscription to {catgr_repr} category',
                body=f'Вы {user} успешно подписались на категорию {catgr_repr}',
                from_email=SERVER_EMAIL,
                to=[email, ],
            )
            html_content = render_to_string(
                'listing/subscription_success.html',
                {
                    'user': user,
                    'category': catgr_repr,
                }
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

        elif not CategorySubs.objects.filter(cat_sub_category_id=catgr.id):
            CategorySubs.objects.create(cat_sub_user_id=user.id, cat_sub_category_id=catgr.id)
            catgr_repr = f'{catgr}'
            email = user.email
            msg = EmailMultiAlternatives(
                subject=f'Subscription to {catgr_repr} category',
                body=f'Вы {user} успешно подписались на категорию {catgr_repr}',
                from_email=SERVER_EMAIL,
                to=[email, ],
            )
            html_content = render_to_string(
                'listing/subscription_success.html',
                {
                    'user': user,
                    'category': catgr_repr,
                }
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

    return redirect('/main/')


@login_required
def remove_subscription(request, pk):
    user = request.user
    catgr = Category.objects.get(id=pk)
    if CategorySubs.objects.filter(linked_user_id=user.id):
        CategorySubs.objects.filter(linked_category_id=catgr.id, linked_user_id=user.id).delete()
    return redirect('/main/')


def add_comment_like(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.like()
    return redirect(request.META.get('HTTP_REFERER'))


def add_comment_dislike(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.dislike()
    return redirect(request.META.get('HTTP_REFERER'))


def update_rating_up(request, pk):
    post = Post.objects.get(id=pk)
    post.like()
    return redirect(request.META.get('HTTP_REFERER'))


def update_rating_down(request, pk):
    post = Post.objects.get(id=pk)
    post.dislike()
    return redirect(request.META.get('HTTP_REFERER'))