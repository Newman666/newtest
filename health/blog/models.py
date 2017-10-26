from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.

class Blog(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200)

	author = models.ForeignKey(User,
							related_name='blogs')
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	#rank = models.DecimalField(max_digits=10, decimal_places=2)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('-created',)

	def get_author_url(self):
		author = self.author
		return author

	def get_absolute_url(self):
		return reverse('blog_detail',
					args=[self.id])