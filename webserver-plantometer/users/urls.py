# DIFFERENT  URL  PATTERNS  ARE  MATCHED  HERE
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as v
from sensors.forms import LoginForm

app_name = 'users'

urlpatterns = [

	url(r'^homepage$', views.homepage, name='homepage'),
	url(r'^loginpage/$', views.signUp, name='loginpage'),
	url(r'^data/$', views.temperature, name='data'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', v.logout , {'next_page': '/'}, name='logout'), 
	url(r'', include('sensors.urls')),
	url(r'^addplant/$', views.addplant, name='addplant'),
	url(r'^settings/$', views.settings, name='settings'),
	url(r'^changepassword/$', views.changepassword, name='changepassword'),
	url(r'^findplants/$', views.findplants, name='findplants'),
	url(r'^delplant/$', views.delplant, name='delplant'),
	url(r'^changeusername/$', views.changeusername, name='changeusername'),
	url(r'^actuatorcontrol/' , views.actuator_control , name='actuatorcontrol'),
	url(r'^changeactuatorcontrol/' , views.change_actuator_control , name='changeActuatorControl'),
	url(r'^changeactuatorlink/' , views.change_actuator_link , name='changeActuatorLink'),
	url(r'^changeplantdetails/' , views.change_plant_details , name='changePlantDetails'),
	url(r'^api/login/$', views.mobile_login, name='mobile_login'),
	url(r'^api/viewPlants/$', views.mobile_addPlants, name='mobile_addPlants'),
	url(r'^api/getCurrent/$', views.mobile_getCurrent, name='mobile_getCurrent'),
	url(r'^api/changeCurrent/$', views.mobile_changeCurrent, name='mobile_changeCurrent'),
	url(r'^api/updateActuator/$', views.mobile_updateActuator, name='mobile_updateActuator'),
	url(r'^api/actuatorOnOff/$', views.mobile_actuatorOnOff, name='mobile_actuatorOnOff'),
]
