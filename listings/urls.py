from django.urls import path

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, SearchResultsListView, \
    add_subscription, remove_subscription


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path('categories/subscribe/category/<int:pk>', add_subscription, name='subscribe_to_category'),
    path('categories/unsubscribe/category/<int:pk>', remove_subscription, name='unsubscribe_to_category'),
]
