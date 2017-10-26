from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import signals



# Create your models here.

class UserType(models.Model):
	user_type = models.CharField(max_length=200,
							db_index=True)
	slug = models.SlugField(max_length=200,
							db_index=True,
							unique=True)
	def __str__(self):
		return self.user_type

class Gender(models.Model):
	user_gender = models.CharField(max_length=200,
							db_index=True)
	slug = models.SlugField(max_length=200,
							db_index=True,
							unique=True)

	def __str__(self):
		return self.user_gender

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	introduction = models.CharField(max_length=400,null=True)
	phone = models.CharField(max_length=200,null=True)
	address = models.CharField(max_length=200, null=True)
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
	gender = models.ForeignKey(Gender,
								related_name="users", null=True)
	user_type = models.ForeignKey(UserType,
								related_name='users', null=True)

	def __str__(self):
		return 'Profile for user {}'.format(self.user.username)

	def get_doctor_url(self):
		user = self.user
		return reverse('doctor_detail',
				args=[user.username])

	def get_type_url(self):
		u_type= self.user_type
		return u_type

class HealthProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	height = models.DecimalField(max_digits=10, decimal_places=0,null=True)
	weight = models.DecimalField(max_digits=10, decimal_places=0,null=True)
	blood_pressure = models.CharField(max_length=200,null=True)
	Blood_sugar = models.DecimalField(max_digits=10, decimal_places=0,null=True)

	def __str__(self):
		return 'Health Profile for user {}'.format(self.user.username)

class MessageBox(models.Model):
	text = models.TextField()
	author = models.ForeignKey(User,related_name="users")
	tosomeone = models.ForeignKey(User,related_name="tosend",default="",null=True)

	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return 'message from {}'.format(self.author)

	def get_author_url(self):
		author = self.author
		return author

	def to(self):
		tosomeone =self.tosomeone
		return tosomeone 

	def get_author(self):
		author = self.author
		return reverse('user_detail',args=[author.username])

class Contact(models.Model):
    user_from = models.ForeignKey(User,related_name='rel_from_set')
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} add {} '.format(self.user_from, self.user_to)


# Add following field to User dynamically
User.add_to_class('bundling',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='doctor',
                                         symmetrical=False))
	

class Message(models.Model):
	sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='message_sender')
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'message_receiver')
	content = models.TextField()

	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def description(self):
		return u'%s send you message <%s>' % (self.sender,self.content)
	class Meta:
		ordering = ('-created_at',)

class Application(models.Model):#Add doctor
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appli_sender')
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'appli_receiver')

	status = models.IntegerField(default = 0)  #application statue 0:view 1:agree 2;disagree
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def description(self):
		return u'%s apply' % self.sender

	class Meta:
		ordering=('-created_at',)

	def get_sender_url(self):
		sender=self.sender
		return sender

	def get_receiver_url(self):
		receiver = self.receiver
		return receiver


class Notice(models.Model):
	sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='notice_sender')							
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='notice_receiver')						
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	event = GenericForeignKey('content_type', 'object_id')
	
	status = models.BooleanField(default=False)	
	type = models.IntegerField()					#notice type  1:patients message 2:patients apply
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	
	class Meta:
		ordering = ('-created_at',)
	
	def __unicode__(self):
		return  u"%sevent: %s" % (self.sender, self.description())
	def description(self):
		  if self.event:
			  return self.event.description()
		  return "No Event"
		
	def reading(self):
		if not status:
			status = True



def application_save(sender, instance,signal, *args, **kwargs):
	entity = instance
	if str(entity.created_at)[:19] == str(entity.updated_at)[:19]:
		event = Notice(sender = enity.sender,receiver= entity.receiver, event = entity, type=1)
		event.save()

def message_save(sender,instance, signal, *args, **kwargs):
	entity = instance
	if str(entity.created_at)[:19] == str(entity.updated_at)[:19]:
		event = Notice(sender=entity.sender,receiver=entity.receiver,event = entity,type=2)
		event.save()

	
signals.post_save.connect(application_save, sender=Message)
signals.post_save.connect(message_save, sender=Application)


