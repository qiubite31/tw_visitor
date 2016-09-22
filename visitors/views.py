# encoding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ArrivalRecord
from django.db.models import Q
import numpy as np
import json
from django.db.models import Sum


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


def get_detail_visitor_data(request, purpose, area):
    # retrieve the certain purpose data
    visitors_purpose = (ArrivalRecord.objects
                        .filter(purpose_cht=purpose)
                        .order_by('report_month')
                        .values('report_month', 'visitor_num',
                                'purpose_cht', 'area_cht')
                        )
    # Filter by area
    visitors_purpose_by_area = visitors_purpose.filter(area_cht=area)
    # Sum by month
    visitors_purpose_sum = (visitors_purpose
                            .values('report_month')
                            .annotate(Sum('visitor_num'))
                            )

    data_list = []
    categories = []
    for visitor_data in visitors_purpose_by_area:
        categories.append(visitor_data['report_month'])
        data_list.append(visitor_data['visitor_num'])

    json_obj = {}
    series = []
    series.append({'name': area, 'data': data_list})
    series.append({'name': '全部',
                   'data': [data['visitor_num__sum']
                            for data in visitors_purpose_sum]})

    json_obj['series'] = series
    json_obj['categories'] = categories
    json_obj['title'] = ({'text': '2016' + area + '地區來臺' + purpose + '旅客人數',
                          'x': -150,
                          'fontFamily': 'Helvetica Neue'})

    return HttpResponse(json.dumps(json_obj))
