from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^post-blog/$', views.post_blog, 
		name='post_blog'),
	url(r'^post-list/$', views.blog_list, 
		name='blog_list'),
	url(r'^blog-detail/(?P<id>\d+)/$', views.blog_detail, 
		name='blog_detail'),
	url(r'^all_post-list/$', views.all_blog_list, 
		name='all_blog_list'),
]