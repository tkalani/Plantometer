from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import os

def home(request):
    return HttpResponse('this is actuator home page')


@method_decorator(csrf_exempt, name='dispatch')
class switch(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('THIS IS GET REQUEST TO switch')

    def post(self, request, *args, **kwargs):
        plant_id = int(request.POST.get("plant_id", ""))
        btn = request.POST.get("btn", "")
        print(plant_id, btn)

        if plant_id == 70:
            if btn == "true":
                os.system('python /home/pi/Desktop/itws/on.py')
            else:
                os.system('python /home/pi/Desktop/itws/off.py')
        elif plant_id == 71:
            if btn == "true":
                os.system('python /home/pi/Desktop/itws/on2.py')
            else:
                os.system('python /home/pi/Desktop/itws/off2.py')

        return JsonResponse({'data': btn})
