from django.urls import path
from .views import index, post_detail, AddPost, post_edit, delete_post, post_draft, published_post, \
    get_category, delete_comment, reviews_views, recommended_posts

    # comment_post


urlpatterns = [
    path('', index, name='index'),
    path('post/draft', post_draft, name='post_draft'),
    path('post/category/<int:category_pk>', get_category, name='get_category'),
    # path('post/comment/<int:post_pk>', comment_post, name='comment_post'),
    path('post/detail/<int:post_pk>', post_detail, name='post_detail'),
    path('post/publish/<int:post_pk>', published_post, name='published_post'),
    path('post/new/', AddPost.as_view(), name='new_post'),
    path('post/edit/<int:post_pk>', post_edit, name='edit_post'),
    path('post/delete/<int:post_pk>', delete_post, name='delete_post'),
    path('post/delete_comment/<int:comment_pk>', delete_comment, name='delete_comment'),
    path('post/reviews/<int:post_pk>', reviews_views, name='reviews_views'),
    path('post/recommended', recommended_posts, name='recommended_posts'),
]