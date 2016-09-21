# encoding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ArrivalRecord
from django.db.models import Q
import numpy as np


def index(request):
    return render(request, 'visitors/index.html', {'status': 'ok'})


def get_country(request, continent):
    countrys = ArrivalRecord.objects.value('area_eng', 'area_cht')
    print(continent)

    country_dict = {}
    for contry in countrys:
        area_eng = country['area_eng']
        area_cht = country['area_cht']
        if area_eng not in country_dict:
            country_dict[area_eng] = area_eng

    context = {
        'countrys': country_dict
    }
    return HttpResponse(context)


def get_area_data(request, purpose, area):
    import json
    from django.db.models import Sum
    visitors_data_by_area = ArrivalRecord.objects.filter(area_cht=area, purpose_cht=purpose).order_by('report_month').values()
    visitors_sum_data = ArrivalRecord.objects.filter(purpose_cht=purpose).order_by('report_month').values('report_month')
    visitors_sum_data = visitors_sum_data.annotate(Sum('visitor_num'))

    data_list = []
    categories = []
    for visitor_data in visitors_data_by_area:
        categories.append(visitor_data['report_month'])
        data_list.append(visitor_data['visitor_num'])

    json_obj = {}
    series = []
    series.append({'name': area, 'data': data_list})
    series.append({'name': '全部', 'data': [data['visitor_num__sum'] for data in visitors_sum_data]})
    json_obj['series'] = series
    json_obj['categories'] = categories
    json_obj['title'] = ({'text': '2016' + area + '地區來臺' + purpose + '旅客人數', 'x': -150})
    # json_obj.append(data_dict)
    # print('大陸')
    # print(json.dumps(json_obj, indent=4))
    return HttpResponse(json.dumps(json_obj))
