

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from posts.views import *

urlpatterns = [
    path('search/',search,name='search'),
    path('admin/', admin.site.urls),
    path('',post_list_view,name='posts'),
    path('post/add/',blog_create,name='add_blog'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('posts/', post_list_view,name='posts'),
    path('profile/',profile_view,name='profile'),
    path('posts/<int:pk>/', post_detail_view, name='post_detail'),
    path('user/<str:username>/',user_view,name='user_detail'),
    path('profile/blockedUsers/',blocked_users_view,name='blocked_users'),
    path('blocked-post/', blocked_post_view, name='blocked_post'),
    path('unblock-user/<str:username>/', unblock_user_view, name='unblock_user'),  
    path('block-user/<str:username>/', block_user_view, name='block_user'), 
    path('profile/edit/',edit_profile_view,name='edit_profile'),
    path('edit-post/<int:pk>/',edit_post_view,name='edit_post'),
    path('edit-comment/<int:pk>/',edit_comment_view,name='edit_comment'),
    path('filterDate/',filterDate,name='filterDate'),
    path('login/',login_view,name='login'),
    path('about/',about_view,name="about"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
