from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login-page', views.login_page, name='login-page'),
    path('logout-page', views.logout_page, name='logout-page'),
    path('register', views.register, name='register'),
    path('blogs', views.blogs, name='blogs'),
    path('add-blog', views.add_blog, name='add-blog'),
    path('delete-blog/<int:pk>', views.delete_blog, name='delete-blog'),
    path('edit-blog/<int:pk>', views.edit_blog, name='edit-blog'),
    path('blog-detail/<int:pk>', views.blog_detail, name='blog-detail'),
]
