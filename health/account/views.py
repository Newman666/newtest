from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, UserTypeForm, HealthProfileEditForm,MessageForm
from .models import Profile, HealthProfile, MessageBox, Contact,Application,Notice,Message
from blog.models import Blog
from common.decorators import ajax_required
from django.template import RequestContext
#from actions.models import Action
#from actions.utils import create_action


def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username=cd['username'], password=cd['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/account/')
				else:
					messages.error(request, 'Disabled account')
	else:
		form = LoginForm()

	return render(request, 'registration/login.html', {'form': form})


def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)

		if user_form.is_valid():
			# Create a new user object but avoid saving it yet
			new_user = user_form.save(commit=False)
			# Set the chosen password
			new_user.set_password(user_form.cleaned_data['password'])
			# Save the User object
			new_user.save()
			# Create the user profile
			profile = Profile.objects.create(user=new_user)
			healthprofile = HealthProfile.objects.create(user=new_user)
			#create_action(new_user, 'has created an account')
			return render(request,
						  'account/register_done.html',
						  {'new_user': new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user,
								 data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile,
									   data=request.POST,
									   files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated successfully')
		else:
			messages.error(request, 'Error updating your profile')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
	return render(request, 'account/edit.html', {'user_form': user_form,
												 'profile_form': profile_form})


@login_required
def dashboard(request):
	# Display all actions by default
	#actions = Action.objects.all().exclude(user=request.user)
	#following_ids = request.user.following.values_list('id', flat=True)
	#if following_ids:
		# If user is following others, retrieve only their actions
		#actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
	#actions = actions[:10]
	user_type = request.user.profile.user_type
	return render(request, 'account/dashboard.html', {'section': 'dashboard','user_type':user_type})


@login_required
def user_list(request):
	users = User.objects.filter(is_active=True)
	return render(request, 'account/user/list.html', {'section': 'doctor',
													  'users': users})


@ajax_required
@require_POST
@login_required
def user_bundle(request):
	user_id = request.POST.get('id')
	action = request.POST.get('action')
	if user_id and action:
		try:
			user = User.objects.get(id=user_id)
			if action == 'bundle':
				Contact.objects.get_or_create(user_from=request.user,
											  user_to=user)
				#create_action(request.user, 'is following', user)
			else:
				Contact.objects.filter(user_from=request.user,
									   user_to=user).delete()
			return JsonResponse({'status':'ok'})
		except User.DoesNotExist:
			return JsonResponse({'status':'ko'})
	return JsonResponse({'status':'ko'})

@login_required
def user_health(request):
	user_id = request.user.id
	user = get_object_or_404(User,id=user_id)
	return render(request,'account/user/healthprofile.html',
							{'user':user})

@login_required
def edit_healthprofile(request):
	if request.method == 'POST':
		healthprofile_form = HealthProfileEditForm(instance=request.user.healthprofile,
													data=request.POST)
		if healthprofile_form.is_valid():
			healthprofile_form.save()
			messages.success(request, 'Health profile updated successfully')
		else:
			messages.error(request, 'Error updating your profile')
	else:
		healthprofile_form = HealthProfileEditForm(instance=request.user.healthprofile)
	return render(request, 'account/edit_healthprofile.html', {'healthprofile_form': healthprofile_form})


@login_required
def user_detail(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	return render(request, 'account/userview/user.html', {'user': user})

@login_required
def doctor_detail(request,username):
	user = get_object_or_404(User, username=username)
	blogs = Blog.objects.filter(author=user)
	author = request.user

	new_message =None
	if request.method=="POST":
		message_form = MessageForm(data=request.POST)	
		if message_form.is_valid():
			new_message = message_form.save(commit=False)
			new_message.author = author 
			new_message.tosomeone= user
			new_message.save()
	else:
		message_form = MessageForm()

	return render(request,
				'account/userview/doctor.html',
				{'user':user,
				'blogs':blogs,
				'new_message':new_message,
				'message_form':message_form})

@login_required
def request_message_list(request):
	user = request.user
	mymessages = MessageBox.objects.filter(tosomeone=user)
	return render(request,'account/user/request_list.html',
				{'mymessages':mymessages})

@login_required
def send_message_list(request):
	user = request.user
	mymessages = MessageBox.objects.filter(author=user)
	return render(request,'account/user/send_list.html',
				{'mymessages':mymessages})

@login_required
def receive_message_list(request):
	user = request.user
	mymessages = MessageBox.objects.filter(tosomeone=user)
	return render(request,'account/user/receive_list.html',
				{'mymessages':mymessages})

@login_required
def send_request_list(request):
	user = request.user
	mymessages = MessageBox.objects.filter(author=user)
	return render(request,'account/user/send_request_list.html',
				{'mymessages':mymessages})


@login_required
def adddoctor(request,sender,receiver):
	sender = User.objects.get(username=sender)
	receiver = User.objects.get(username=receiver)
	application = Application(sender=sender,receiver=receiver,status=0)
	application.save()
	return render(request,'account/dashboard.html')

@login_required
def shownotice(request):
	notice_list = Notice.objects.filter(receiver = request.user,status= False)
	return render(request,'account/user/request_list.html',
		{'notice_list':notice_list})

def noticedetail(request,pk):
	pk=int(pk)
	notice = Notice.objects.gte(pk=pk)
	notice.status = True
	notice.save()
	message_id = notice.event.id
	return HttpResponseRedirect(reverse_lazy('message_detail',kwargs = {'pk':message_id}))

#1 agree 2 disagree
def doctoragree(request,pk,flag):
	flag = int(flag)
	pk = int(pk)
	entity = Notice.objects.get(pk=pk)
	entity.status = True
	application = entity.event
	application.status=flag


	application.save()
	entity.save()

	if flag == 1:
		str = 'success'
	else:
		str = 'refuse'
	return render(request, 'account/user/request_list.html')

@login_required
def patient_list(request):

	user = request.user
	users = Application.objects.filter(status=1)

	return render(request, 'account/doctor/patient_list.html',
		{'users':users})

@login_required
def mydoctor_list(request):
	user = request.user
	users = Application.objects.filter(status = 1)
	return render(request, 'account/user/mydoctor_list.html',{'users':users})

