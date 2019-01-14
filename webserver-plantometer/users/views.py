from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from .models import Users, Plants
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.utils.decorators import method_decorator
import json
import requests

userid = -1
def homepage(request):
	return render(request, 'users/index.html')

def loginpage(request):
	return render(request, 'users/login.html')

def temperature(request):
	return render(request, 'users/index.html')

#  SIGN UP FUNCTIONS
def signUp(request):
	if request.POST:
		t = Users(name=request.POST['name'],password=request.POST['password'],phone=request.POST['username'],address=request.POST['address'])
		t.save()		
		return redirect('../login')
	return render(request, 'users/loginpage.html')

#  VALIDATES  WHETHER  THE  INFORMATION  ENTERED  IS  A  VALID  ONE  AND  THEN  RENDERS  DASHBOARD  PAGE  OF  THE  USER (SENSORS/TEMPERATURE.HTML)
def login(request):
	r = False
	if request.POST:
		t = Users.objects.filter(password=request.POST['password'],phone=request.POST['username'])
		if len(t):
			request.session['name'] = t[0].name
			request.session['id'] = t[0].id
			global userid
			userid = t[0].id
			return redirect('../../sensors/data')
		else:
			messages.error(request, 'no such user')
			return render(request, 'users/login.html')
	return render(request, 'users/login.html',{"r":r})


#  ENTERS  RECORD  OF  NEW  PLANT  ADDED  WITH  CONTACTS  OF  IT'S  OWNER  AND  LOCATION
def addplant(request):
	r = False
	if request.POST:
		global userid
		z = get_object_or_404(Users, pk=userid)
		f = Plants.objects.filter(userid = z)
		if f:
			p = Plants(userid = z, plantname = request.POST['plantname'], latitude = request.POST['latitude'], longitude = request.POST['longitude'])
			p.save()
		else:
			p = Plants(userid = z, plantname = request.POST['plantname'], latitude = request.POST['latitude'], longitude = request.POST['longitude'])
			p.save()
			z.currentplant = p.id
			z.save()
		z = Plants.objects.filter(userid = userid)
		return redirect('../../users/addplant/')
	return render(request, 'users/addplant.html')

@csrf_exempt
def actuator_control(request):

	pid = request.POST.get('plant_id', None)
	btn = request.POST.get('btn', None)
	plant = get_object_or_404(Plants, pk=pid)
	link = plant.actuatorlink
	print(pid, btn, link)
	print(type(pid), type(btn),type(link))
	json_data = 'failed'
	try:
		response = requests.post(link , data={"plant_id": pid, "btn": btn})
		print(json.loads(response.text)['data'])
		json_data = "done"
		print(json_data)
	except: 
		json_data = 'failed'

	if json_data == 'done':
		if btn == 'true':
			plant.actuatorstatus = 1
		else:
			plant.actuatorstatus = 0
		plant.save()
		return JsonResponse({'res': "done"})
	else:
		return JsonResponse({'res': "failed"})

def settings(request):
	return render(request, 'users/settings.html')

@method_decorator(csrf_exempt, name='dispatch')
def changepassword(request):
	oldPassword = request.POST.get('oldPassword', None)
	newPassword1 = request.POST.get('newPassword1', None)
	newPassword2 = request.POST.get('newPassword2', None)
	global userid
	u = Users.objects.filter(id = userid)
	if oldPassword != u[0].password:
		context = {
			'data' : 0
		}
		res = JsonResponse(context)
		res['Access-Control-Allow-Origin']="*"
		return res
	else:
		z = get_object_or_404(Users, pk=userid)
		z.password = newPassword1
		z.save()
		context = {
			'data' : 1
		}
		res = JsonResponse(context)
		res['Access-Control-Allow-Origin']="*"
		return res

def findplants(request):
	global userid
	u = get_object_or_404(Users, pk=userid)
	phone = u.phone
	p = Plants.objects.filter(userid = u)
	count = p.count()
	pid = []
	name = []
	lat = []
	lng = []
	actuator_control = []
	actuator_link = []
	for i in range(count):
		pid.append(p[i].id)
		name.append(p[i].plantname)
		lat.append(p[i].latitude)
		lng.append(p[i].longitude)
		actuator_control.append(p[i].actuatorcontrol)
		actuator_link.append(p[i].actuatorlink)
	context = {
		'pid' : pid,
		'name' : name,
		'count' : count,
		'lat' : lat,
		'lng' : lng,
		'username' : phone,
		'act_ctrl' : actuator_control,
		'act_link' : actuator_link,
	}
	res = JsonResponse(context)
	res['Access-Control-Allow-Origin']="*"
	return res

@method_decorator(csrf_exempt, name='dispatch')
def delplant(request):
	pid = request.POST.get('pid', None)
	global userid
	user = get_object_or_404(Users, pk=userid)
	Plants.objects.filter(id=int(pid)).delete()
	if user.currentplant == int(pid):
		p = Plants.objects.filter(userid = user)
		print(p)
		if p:
			print(p[0].id)
			user.currentplant = p[0].id
			user.save()
		else:
			user.currentplant = -1
			user.save()
	context = {
		'data':1
	}
	res = JsonResponse(context)
	res['Access-Control-Allow-Origin']="*"
	return res

@method_decorator(csrf_exempt, name='dispatch')
def changeusername(request):
	p = request.POST.get('new_username', None)
	t = Users.objects.filter(phone = p)
	if t:
		context = {
		'data':0
		}
	else:
		global userid
		z = get_object_or_404(Users, pk=userid)
		z.phone = p
		z.save()
		context = {
		'data':1
		}
	res = JsonResponse(context)
	res['Access-Control-Allow-Origin']="*"
	return res


@method_decorator(csrf_exempt, name='dispatch')
def change_actuator_control(request):
	plant = request.POST.get('pid', None)
	ctrl = request.POST.get('control', None)
	print(plant, ctrl)
	p = get_object_or_404(Plants, id=int(plant))
	p.actuatorcontrol = int(ctrl)
	p.save()
	context = {
		'data' : 1
	}
	res = JsonResponse(context)
	res['Access-Control-Allow-Origin']="*"
	return res

def change_actuator_link(request):
	plant = request.POST.get('pid', None)
	link = request.POST.get('link', None)
	print(plant, link)
	p = get_object_or_404(Plants, id=int(plant))
	p.actuatorlink = str(link)
	p.save()
	context = {
		'data' : 1
	}
	res = JsonResponse(context)
	res['Access-Control-Allow-Origin']="*"
	return res

def change_plant_details(request):
	plant = request.POST.get('pid', None)
	latitude = request.POST.get('lat', None)
	longitude = request.POST.get('lng', None)
	name = request.POST.get('plantname', None)
	print(plant, latitude, longitude, name)
	p = get_object_or_404(Plants, id=int(plant))
	p.plantname = name
	p.latitude = latitude
	p.longitude = longitude
	p.save()
	context = {
		'data': 1
	}
	res = JsonResponse(context)
	res['Access-Control-Allow-Origin']="*"
	return res

# ----------------- API --------------------

@csrf_exempt
def mobile_login(request):
	if request.method=='POST':
		print("post successfull")
		jsonResponse=json.loads(request.body.decode('utf-8'))
		username=jsonResponse['json_data']['username']
		password=jsonResponse['json_data']['password']
		print("Authentic")
		print(password)
		t = Users.objects.filter(password=password,phone=username)

		if len(t):
			print("Authentic")
			#request.session['name'] = t[0].name
			#request.session['id'] = t[0].id

			global userid
			userid = t[0].id
			u={"pass":"true","id":t[0].id,"name":t[0].name,"phone":t[0].phone,"address":t[0].address,"currentplant":t[0].currentplant}
			print(u)
			return JsonResponse(u)
		else:
			u={"pass":"false"}
			print(u)
			return JsonResponse(u)
	if request.method=='GET':
		return HttpResponse("<h1>hi</h1>")

@csrf_exempt
def mobile_addPlants(request):
	if request.method=='POST':
		print("hiii")
		jsonResponse=json.loads(request.body.decode('utf-8'))
		id=jsonResponse['id']
		z = Plants.objects.filter(userid = id)
		count=z.count()
		d={}
		l=[]
		l3=[]
		for i in range(count):
			l3.append([z[i].id,z[i].plantname])
			d[z[i].id]=z[i].plantname
		print(d)
		return JsonResponse(d)

@csrf_exempt
def mobile_getCurrent(request):
	if request.method=='POST':
		print("ingetcurrent------------------")
		d={}
		print("hi")
		t = Users.objects.filter(id=5)
		print(t)
		d["id"]=t[0].currentplant
		z=Plants.objects.filter(userid = 5)
		print(z)
		for i in range(z.count()):

			if(z[i].id==t[0].currentplant):
				d["actuatorcontrol"]=z[i].actuatorcontrol
				d["actuatorstatus"]=z[i].actuatorstatus
				d["actuatorlink"]=z[i].actuatorlink
		
		print(d)
		return JsonResponse(d)
		#print (t[0].currentplant)
@csrf_exempt
def mobile_changeCurrent(request):
	if request.method=='POST':
		jsonResponse=json.loads(request.body.decode('utf-8'))
		curPlant=jsonResponse['cp']
		userid=jsonResponse['id']
		print(userid,curPlant)
		t = Users.objects.filter(id=userid)[0];
		t.currentplant=curPlant;
		t.save();
		z=Plants.objects.filter(userid = 5)
		d={}
		print("z-----------------",z)
		for i in range(z.count()):

			if(z[i].id==curPlant):
				d["actuatorcontrol"]=z[i].actuatorcontrol
				d["actuatorstatus"]=z[i].actuatorstatus
				d["actuatorlink"]=z[i].actuatorlink
		return JsonResponse(d)
@csrf_exempt
def mobile_updateActuator(request):
	if request.method=='POST':
		jsonResponse=json.loads(request.body.decode('utf-8'))
		curPlant=jsonResponse['curPlant']
		mode=jsonResponse['mode']
		id=jsonResponse['id']
		print("dets=",mode,curPlant)
		p = get_object_or_404(Plants, id=int(curPlant))
		p.actuatorcontrol = int(mode)
		p.save()
		return JsonResponse({})		

@csrf_exempt
def mobile_actuatorOnOff(request):
	if request.method=='POST':
		
		jsonResponse=json.loads(request.body.decode('utf-8'))
		btn2=jsonResponse['mode']
		pid2=jsonResponse['curPlant']
		btn3=str(btn2)
		btn=""
		for i in range(len(btn3)):
			btn+=btn3[i].lower()
		print(btn)
		pid=str(pid2)
		plant = get_object_or_404(Plants, pk=pid)
		link = plant.actuatorlink
		print(pid, btn, link)
		print(type(pid), type(btn),type(link))
		json_data = 'failed'
		try:
			response = requests.post(link , data={"plant_id": pid, "btn": btn})
			json_data = "done"
		except: 
			json_data = 'failed'

		if json_data == 'done':
			if btn == 'true':
				plant.actuatorstatus = 1
			else:
				plant.actuatorstatus = 0
			plant.save()
			return JsonResponse({'res': "done"})
		else:
			return JsonResponse({'res': "failed"})