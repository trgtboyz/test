from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import ReverseIP
from datetime import date
import requests
import json
URL = 'https://nominatim.openstreetmap.org/reverse?format=json&addressdetails=0'

# Create your views here.
def reverse_address(request,latitude=None,longitude=None):
    try:
        if latitude == None or longitude == None:
            return JsonResponse({'status':'failed','error':'No latitude or longitude specified'})
        else:
            today = date.today()
            ins_check = ReverseIP.objects.filter(dbl_latitude = latitude,dbl_longitude = longitude,dat_created = today).values('txt_address')
            if ins_check:
                return HttpResponse(json.dumps({'name':ins_check[0]['txt_address']}, ensure_ascii=False), content_type="application/json")
            else:
                current_url = URL + '&lat=' + latitude + '&lon=' + longitude
                r = requests.get(url = current_url)
                data = r.json()
                address = data['display_name']
                ins_check = ReverseIP.objects.filter(dbl_latitude = latitude,dbl_longitude = longitude)
                if ins_check:
                    ins_check.update(txt_address = address,dat_created = today)
                else:
                    ReverseIP.objects.create(
                    dbl_latitude = latitude,dbl_longitude = longitude,dat_created = today,txt_address = address
                    )
                return HttpResponse(json.dumps({'name':address}, ensure_ascii=False), content_type="application/json")
    except Exception as e:
        return JsonResponse({'status':'failed','error':str(e)})
