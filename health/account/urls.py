from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete


urlpatterns = [
	url(r'^login/$', views.user_login, name='login'),
	url(r'^$', views.dashboard, name='dashboard'),

	url(r'^register/$', views.register, name='register'),
	url(r'^edit/$', views.edit, name='edit'),

	# login / logout urls
	#url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
	url(r'^logout/$', logout, name='logout'),
	url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),

	# change password urls
	url(r'^password-change/$', password_change, name='password_change'),
	url(r'^password-change/done/$', password_change_done, name='password_change_done'),

	# restore password urls
	url(r'^password-reset/$', password_reset, name='password_reset'),
	url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
	url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
	url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),

	# user profiles
	url(r'^users/$', views.user_list, name='user_list'),
	url(r'^users/bundle/$', views.user_bundle, name='user_bundle'),
	url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),

	url(r'^healthprofile/$', views.user_health, name="user_health"),
	url(r'^edit-your-health-profile/$', views.edit_healthprofile, name='edit_healthprofile'),
	url(r'^doctor/(?P<username>[-\w]+)/$', views.doctor_detail, name='doctor_detail'),
	url(r'^request-message-list/$', views.request_message_list, 
		name='request_message_list'),
	url(r'^send-message-list/$', views.send_message_list, 
		name='send_message_list'),
	url(r'^receive-message-list/$', views.receive_message_list, 
		name='receive_message_list'),
	url(r'^send-request-list/$', views.send_request_list, 
		name='send_request_list'),

	url(r'^patient-list/$', views.patient_list, 
		name='patient_list'),

	url(r'^adddoctor/(?P<sender>\w+)/(?P<receiver>\w+)/$', views.adddoctor, name='adddoctor'), 

	url(r'^show_notice/$', views.shownotice, name='show_notice'),

	url(r'^doctoragree/(?P<pk>\d+)/(?P<flag>\d+)/$', views.doctoragree, name='doctoragree'),#pk涓哄鏂圭敤鎴穒d

	url(r'^patient-list/$', views.patient_list, 
		name='patient_list'),

	url(r'^mydoctor-list/$', views.mydoctor_list, 
		name='mydoctor_list'),


	
]