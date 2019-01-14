#VARIOUS  URL  PATTERNS  ARE  MATCHED  HERE
from django.conf.urls import url
from . import views
from django.contrib.auth import views as v
app_name = 'sensors'

urlpatterns = [
	
    url(r'^dataupdate/$', views.data_update, name = 'dataupdate'),
    url(r'^data/logout/$', v.logout , {'next_page': '/'}, name='logout'),
    url(r'^pdetail/$',views.DetailView,name='pdetail'),
    url(r'^updateplant/$', views.updateplant_overview, name = 'setplant'),
    url(r'^plantdetail/' , views.plantdetail , name='plantdetail' ),

    url(r'^overview/' , views.overview , name='overview'),
    url(r'^detail/' , views.detail , name='detail'),
    url(r'^gearth/' , views.gearth , name='gearth'),

    url(r'^logdata/$', views.sensor_data.as_view(), name = 'sensor_data'),
    url(r'^data/$', views.show_list, name = 'data'),

    url(r'^databydate/$',views.dataByDate,name='databydate'),
    url(r'^api/dataByDate/$', views.mobile_dataByDate, name='mobile_dataByDate'),
]
