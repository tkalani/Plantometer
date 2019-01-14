from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import weathersensors, plantsensors, reservoir
from users.models import Plants, Users
from django.views import generic
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers
import time
import os
import requests
import json
userid = -1
plant_id = -1

@method_decorator(csrf_exempt, name='dispatch')
class sensor_data(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('THIS IS GET REQUEST TO LOGDATA')

    def post(self, request, *args, **kwargs):
        humidity = request.POST.get("humidity", "")
        temp = request.POST.get("temp", "")
        rain = request.POST.get("rain", "")
        distance = float(request.POST.get("distance", ""))
        distance = ((12.0-distance)/12.0)*100.0
        soilmoist = request.POST.get("soilmoist", "")
        if float(soilmoist) < 0:
            soilmoist = str(0)
        pressure = request.POST.get("pressure", "")
        altitude = request.POST.get("altitude", "")
        seapressure = request.POST.get("seapressure", "")
        user_id = request.POST.get("user_id", "")
        plant_name = request.POST.get("plant_name", "")
        p = Users.objects.filter(id=user_id)[0]
        plant_id = request.POST.get("plant_id", "")
        
        w = weathersensors(rain = rain, temp = temp, humidity = humidity, pressure = pressure, altitude = altitude, seapressure = seapressure, userid = user_id, plant_id = plant_id, time = time.strftime("%X"), date = time.strftime("%Y-%m-%d"))
        w.save()
        entryid = w.id
        s = weathersensors.objects.filter(pk=w.id)[0]
        
        p = plantsensors(entryid = s, soilmoisture = soilmoist)
        p.save()
        
        r = reservoir(entryid = s, distance = distance)
        r.save()

        plantobj = get_object_or_404(Plants, pk=plant_id)
        if plantobj.actuatorcontrol == 0:
            automaticControl(request, plant_id, float(soilmoist), float(rain))

        return HttpResponse('DONE')

#  IF  THE  USER  HAS  SUCCESSFULLY  LOGGED  IN  THIS  FUNCTION  RENDERS  TO TEMPERATURE.HTML
def show_list(request):
    if 'name' in request.session:
        global userid
        userid = request.session['id']
        f = Users.objects.filter(id = userid)
        return render(request, 'sensors/main.html', { "userdata": f[0]})
    else:
        return redirect('../../users/login')


#  THE  Rxjx  FUNCTION  IN  TEMPERTURE.HTML  USER  THIS  FUNCTION  TO  RETRIEVE  DATA  FROM  DATBASE  IN  CERTAIN  INTERVAL OF  TIME  PERIODICALLY
def data_update(request):
    global userid
    p = Users.objects.filter(id = userid)[0]
    li = weathersensors.objects.filter(userid=userid)
    li = li.filter(plant_id = p.currentplant)

    plantobj = get_object_or_404(Plants, pk=p.currentplant)
    linkbool = 1
    if plantobj.actuatorlink == "-1":
        linkbool = -1

    if li.count()>=1:
        entry = li[li.count()-1].id
        c = weathersensors.objects.filter(id = entry)
        d = plantsensors.objects.filter(entryid = entry)
        e = reservoir.objects.filter(entryid = entry)

        data = {
            'temp' : c[0].temp,
            'humidity' : c[0].humidity,
            'pressure' : c[0].pressure,
            'userid' : c[0].userid,
            'date' : c[0].date,
            'time' : c[0].time,
            'soilmoist' : d[0].soilmoisture,
            'distance' : e[0].distance,
            'data' : 1,
            'rain' : c[0].rain,
            'actuatorstatus' : plantobj.actuatorstatus,
            'actuatorcontrol' : plantobj.actuatorcontrol,
            'actuatorlink': linkbool,
        }
        res = JsonResponse(data)
        return res 
    else:
        data = {
            'data' : 0,
            'actuatorstatus' : plantobj.actuatorstatus,
            'actuatorcontrol' : plantobj.actuatorcontrol,
            'actuatorlink': linkbool,
        }
        res = JsonResponse(data)
        return res 

#  WHENEVER    PLANT  NAME  IS  CLICKED  ON  TEMPERATIRE.HTML  A  DETAIL.HTML  IS  RENDERED  CONTAINING  SENSOR  DATA  FOR  THAT  PLANT    
def DetailView(request):
    pid = request.POST.get('pid', None)
    print("hi i am here")
    global userid
    w = weathersensors.objects.filter(userid = userid)
    w = w.filter(plant_id = pid)
    if w.count() >= 20:
        temp = []
        humidity = []
        time = []
        date = []
        soilmoisture = []
        distance = []
        actualheight = []
        k = w.count()
        i = 1
        while i <= 20:
            temp.append(w[k-i].temp)
            humidity.append(w[k-i].humidity)
            time.append(w[k-i].time)
            date.append(w[k-i].date)
            s = plantsensors.objects.filter(entryid = w[k-i])
            soilmoisture.append(s[0].soilmoisture)
            s = reservoir.objects.filter(entryid = w[k-i])
            height = float(s[0].distance)
            distance.append(height)
            actualheight.append(s[0].actualHieght)
            i += 1
        context = {
                'temp' : temp,
                'humidity' : humidity,
                'date' : date,
                'time' : time,
                'soilmoist' : soilmoisture,
                'distance' : distance,
                'pid' : pid,
                'data' : 1
            }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin']="*"
        return res
        #return render(request, 'sensors/detail.html',context)   
    else:
        context = {
            'data' : 0
        }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin']="*"
        return res
        #return render(request, 'sensors/detail.html',context)

def updateplant_overview(request):
    if request.POST:
        global userid
        z = Users.objects.filter(id=userid)[0]
        global plantid
        plantid = z.currentplant
        z.currentplant = request.POST['currentplant']
        z.save()
    return redirect('../overview')

def validate(curdate):
    curdate = str(curdate)
    d = curdate.split('-')
    if int(d[2]) == 0:
        if int(d[1]) == 2:
            d[1] = 1
            d[2] = 31
        elif int(d[1]) == 3:
            d[1] = 2
            d[2] = 28
        elif int(d[1]) == 4:
            d[1] = 3
            d[2] = 31
        elif int(d[1]) == 5:
            d[1] = 4
            d[2] = 30
        elif int(d[1]) == 6:
            d[1] = 5
            d[2] = 31
        elif int(d[1]) == 7:
            d[1] = 6
            d[2] = 30
        elif int(d[1]) == 8:
            d[1] = 7
            d[2] = 31
        elif int(d[1]) == 9:
            d[1] = 8
            d[2] = 31
        elif int(d[1]) == 10:
            d[1] = 9
            d[2] = 30
        elif int(d[1]) == 11:
            d[1] = 10
            d[2] = 31
        elif int(d[1]) == 12:
            d[1] = 11
            d[2] = 30
        elif int(d[1]) == 1:
            d[0] = int(d[0])-1
            d[1] = 12
            d[2] = 31
    da = str(d[2])
    m = str(d[1])
    y = str(d[0])
    curdate = str(y+'-'+m+'-'+da)
    return curdate


def collectData(pid, option, endval):
    option = 0
    d = str(time.strftime("%Y-%m-%d"))
    j = 0
    temparray = []
    soilmoistarray = []
    humidityarray = []
    levelarray = []
    datearray = []
    while option != endval:
        d = d.split('-')
        d[2] = str(int(d[2])-j)
        d = str('-'.join(d))
        curdate = time.strftime(d)
        curdate = validate(curdate)
        d = curdate
        w = weathersensors.objects.filter(userid = userid)
        w = w.filter(plant_id = pid)
        w = w.filter(date = curdate)
        k = w.count()
        temp = 0
        humidity = 0
        soilmoist = 0
        level = 0
        if k == 1:
            temp = w[0].temp
            humidity = w[0].humidity
            s = plantsensors.objects.filter(entryid = w[0])
            s1 = reservoir.objects.filter(entryid = w[0])
            soilmoist = s[0].soilmoisture
            level = s1[0].distance
        elif k == 0:
            temp = 0
            humidity = 0
            soilmoist = 0
            level = 0
        else:
            for i in range(1, k+1):
                s = plantsensors.objects.filter(entryid = w[k-i])
                s1 = reservoir.objects.filter(entryid = w[k-i])
                temp += w[k-i].temp
                humidity += w[k-i].humidity
                soilmoist += s[0].soilmoisture
                level += s1[0].distance
            temp = temp/k;
            humidity = humidity/k
            soilmoist = soilmoist/k
            level = level/k
        option += 1
        if j == 0:
            j = 1
        temparray.append(temp)
        humidityarray.append(humidity)
        soilmoistarray.append(soilmoist)
        levelarray.append(level)
        datearray.append(curdate)
    context = {
            'temp' : temparray,
            'humidity' : humidityarray,
            'date' : datearray,
            'soilmoist' : soilmoistarray,
            'distance' : levelarray,
            'pid' : pid,
            'data' : 1
        }
    res = JsonResponse(context)
    res['Access-Control-Allow-Origin']="*"
    return res

def dataByDate(request):
    pid = request.POST.get('pid', None)
    option = request.POST.get('option', None)
    if option == '2':
        return collectData(pid, option, 7)
    elif option == '3':
        return collectData(pid, option, 15)
    else:
        return collectData(pid, option, 30)

#  THIS  FUNCTION  IS  CALLED  BY  THE  AJAX  FUNCTION  BY  GOOGLE  EARTH  API  IN TEMPERATURE.HTML
#  IT  RETURNS  THE  OCATION (  LATITUDE,  LONGITUDE  )  OF  EVERY  PLANT  REGISTERED  WITH THE  USER  
def plantdetail(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        global userid
        data = { 'plant_detail': serializers.serialize('json', Plants.objects.filter(userid = userid)) }
        res = JsonResponse(data)
        res['Access-Control-Allow-Origin']="*"
        return res

def gearth(request):
    
    os.system('rmdir kkk')
    return render(request, 'sensors/gearth.html')

def overview(request):
    if 'name' in request.session:
        global userid
        userid = request.session['id']
        z = Plants.objects.filter(userid = userid)
        f = Users.objects.filter(id = userid)
        cp = f[0].currentplant
        d = z.filter(pk = cp)[0]
        return render(request, 'sensors/data.html', { "plant_names" : z, "userdata": f[0]})
    else:
        return HttpResponse('error')

def detail(request):
    if 'name' in request.session:
        global userid
        userid = request.session['id']
        z = Plants.objects.filter(userid = userid)
        f = Users.objects.filter(id = userid)
        return render(request, 'sensors/detail.html', { "plant_names" : z, "userdata": f[0]})
    else:
        return HttpResponse('error')

def automaticControl(request, plant_id, soilmoisture, rain):

    on = 'false'
    if soilmoisture <= 35 and rain == 0:
        on = 'true'

    url1 = "http://plantometer.pythonanywhere.com/users/actuatorcontrol/"
    url2 = "http://127.0.0.1:8000/users/actuatorcontrol/"

    link = url1

    json_data = 'failed'
    response = requests.post(link , data={"plant_id": plant_id, "btn": on})
    print(list(response)[:10])


# ----------------------------------------------------- API -------------------------------------------------------

def DetailView2(curPlant, id):
    pid = curPlant
    print("hi i am here", pid)
    #global userid
    w = weathersensors.objects.filter(userid = id)
    w = w.filter(plant_id = pid)
    print(w.count())
    if w.count() >= 10:
        temp = []
        humidity = []
        time = []
        date = []
        soilmoisture = []
        distance = []
        actualheight = []
        k = w.count()
        i = 1
        while i <= 20:
            temp.append(w[k-i].temp)
            humidity.append(w[k-i].humidity)
            time.append(w[k-i].time)
            date.append(w[k-i].date)
            s = plantsensors.objects.filter(entryid = w[k-i])
            soilmoisture.append(s[0].soilmoisture)
            s = reservoir.objects.filter(entryid = w[k-i])
            height = float(s[0].distance)
            distance.append(height)
            actualheight.append(s[0].actualHieght)
            i += 1
        context = {
                'temp' : temp,
                'humidity' : humidity,
                'date' : date,
                'time' : time,
                'soilmoist' : soilmoisture,
                'distance' : distance,
                'pid' : pid,
                'data' : 1
            }
        return context
        #return render(request, 'sensors/detail.html',context)   
    else:
        context = {
            'data' : 0
        }
        return context


def collectData2(pid, option, endval):
    option = 0
    d = str(time.strftime("%Y-%m-%d"))
    j = 0
    temparray = []
    soilmoistarray = []
    humidityarray = []
    levelarray = []
    datearray = []
    while option != endval:
        d = d.split('-')
        d[2] = str(int(d[2])-j)
        d = str('-'.join(d))
        curdate = time.strftime(d)
        curdate = validate(curdate)
        d = curdate
        w = weathersensors.objects.filter(userid = userid)
        w = w.filter(plant_id = pid)
        w = w.filter(date = curdate)
        k = w.count()
        temp = 0
        humidity = 0
        soilmoist = 0
        level = 0
        if k == 1:
            temp = w[0].temp
            humidity = w[0].humidity
            s = plantsensors.objects.filter(entryid = w[0])
            s1 = reservoir.objects.filter(entryid = w[0])
            soilmoist = s[0].soilmoisture
            level = s1[0].distance
        elif k == 0:
            temp = 0
            humidity = 0
            soilmoist = 0
            level = 0
        else:
            for i in range(1, k):
                s = plantsensors.objects.filter(entryid = w[k-i])
                s1 = reservoir.objects.filter(entryid = w[k-i])
                temp += w[k-i].temp
                humidity += w[k-i].humidity
                soilmoist += s[0].soilmoisture
                level += s1[0].distance
            temp = temp/k;
            humidity = humidity/k
            soilmoist = soilmoist/k
            level = level/k
        option += 1
        if j == 0:
            j = 1
        temparray.append(temp)
        humidityarray.append(humidity)
        soilmoistarray.append(soilmoist)
        levelarray.append(level)
        datearray.append(curdate)
    context = {
            'temp' : temparray,
            'humidity' : humidityarray,
            'date' : datearray,
            'soilmoist' : soilmoistarray,
            'distance' : levelarray,
            'pid' : pid,
            'data' : 1
        }
    return (context)


@csrf_exempt
def mobile_dataByDate(request):
    if request.method=='POST':
        jsonResponse=json.loads(request.body.decode('utf-8'))
        option=jsonResponse['option']
        userid=jsonResponse['id']
        curPlant=jsonResponse['curPlant']
        d={}
        print(userid,curPlant,option)
        if option == '1' or option==1:
            d=DetailView2(curPlant,5)
            print ("option1", DetailView2(curPlant,5))
        if option == '2' or option==2:
            d=collectData2(curPlant, option, 7)
            print ("option2",collectData2(curPlant, option, 7))
        elif option == '3' or option==3:
            d=collectData2(curPlant, option, 15)
            print ("option3",collectData2(curPlant, option, 15))
        elif option== '4' or option==4:
            d=collectData2(curPlant, option, 30)
            print ("option4",collectData2(curPlant, option, 30))
        # t = Users.objects.filter(id=userid)[0];
        # t.currentplant=curPlant;
        # t.save();
        
        d["done"]=True
        return JsonResponse(d)
