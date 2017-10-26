from django.shortcuts import render, get_object_or_404
from .forms import BlogForm
from .models import Blog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_blog(request):
	
	author = request.user
	new_blog =None
	if request.method=="POST":
		blog_form = BlogForm(data=request.POST)	
		if blog_form.is_valid():
			new_blog = blog_form.save(commit=False)
			new_blog.author = author 
			new_blog.save()
	else:
		blog_form = BlogForm()

	return render(request,
				'blogs/post.html',
				{'author':author,
				'new_blog':new_blog,
				'blog_form':blog_form})


def blog_list(request):
	author = request.user.id

	blogs = Blog.objects.filter(author_id=author)

	paginator = Paginator(blogs, 6)
	page = request.GET.get('page')
	try:
		blogs = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		blogs = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
			# If page is out of range deliver last page of results
			blogs = paginator.page(paginator.num_pages)
		if request.is_ajax():
			return render(request,
					'blogs/list_ajax.html',
					{'blogs': blogs})

	return render(request,
			'blogs/blog_list.html',
			{'blogs': blogs,
			'page': page})

def blog_detail(request,id):
	blog = get_object_or_404(Blog, id=id)

	author = request.user
	return render(request,
				'blogs/blog_detail.html',
				{'blog':blog,
				'author':author})

def all_blog_list(request):
	blogs = Blog.objects.all()

	paginator = Paginator(blogs, 6)
	page = request.GET.get('page')
	try:
		blogs = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		blogs = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
			# If page is out of range deliver last page of results
			blogs = paginator.page(paginator.num_pages)
		if request.is_ajax():
			return render(request,
					'blogs/blog_list_ajax.html',
					{'blogs': blogs})

	return render(request,
			'blogs/blog_list.html',
			{'blogs': blogs,
			'page': page,
			'section':'blog'})
