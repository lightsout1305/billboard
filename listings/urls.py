from django.urls import path

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, SearchResultsListView, \
    add_subscription, remove_subscription, CategoryDetail, add_comment_like, add_comment_dislike, update_rating_up, update_rating_down


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path('categories/', CategoryDetail.as_view(), name='test'),
    path('categories/subscribe/category/<int:pk>', add_subscription, name='subscribe_to_category'),
    path('categories/unsubscribe/category/<int:pk>', remove_subscription, name='unsubscribe_to_category'),
    path('plusratingcomment/<int:pk>/', add_comment_like, name='add_comment_like'),
    path('minusratingcomment/<int:pk>/', add_comment_dislike, name='add_comment_dislike'),
    path('pluscontent/<int:pk>/', update_rating_up, name='add_content_like'),
    path('minuscontent/<int:pk>/', update_rating_down, name='add_content_dislike'),
]
