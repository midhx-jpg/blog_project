from django.urls import path
from .views import (
    CustomLoginView, CustomLogoutView, signup, profile_view,
    blog_list_byuser, create_post, update_post_view, delete_post_view,blog_detail_view,index
)

urlpatterns=[
    path('login/', CustomLoginView.as_view(next_page="/"), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('blog_list_byuser', blog_list_byuser, name='blog_list_byuser'),
    path('post/<int:id>/', blog_detail_view, name='blog_detail'),  # View single post
    path('post/create/', create_post, name='create_post'),  # Create new post
    path('post/<int:id>/edit/', update_post_view, name='update_post'),  # Update post
    path('post/<int:id>/delete/', delete_post_view, name='delete_post'),


]