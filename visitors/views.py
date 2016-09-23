# encoding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ArrivalRecord
from django.db.models import Q
import numpy as np
import json
from django.db.models import Sum
from collections import OrderedDict


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
    if not area == '前五地區':
        visitors_purpose_by_area = visitors_purpose.filter(area_cht=area)
        data_dict = {}
        categories = []
        for visitor_data in visitors_purpose_by_area:
            data_dict.setdefault(area, []).append(visitor_data['visitor_num'])
            categories.append(visitor_data['report_month'])
    else:
        visitors_area_sum = (visitors_purpose
                             .values('area_cht')
                             .annotate(Sum('visitor_num'))
                             .order_by('-visitor_num__sum')
                             )
        area_top5 = []
        for idx, data in enumerate(visitors_area_sum):
            if idx > 4:
                break
            area_top5.append(data['area_cht'])
        # print(area_top10)
        visitors_purpose_by_area_top5 = visitors_purpose.filter(area_cht__in=area_top5)
        data_dict = OrderedDict()
        categories = []
        for area_key in area_top5:
            data_dict[area_key] = []

        for visitor_data in visitors_purpose_by_area_top5:
            # print(visitor_data['area_cht'])
            categories.append(visitor_data['report_month'])
            data_dict[visitor_data['area_cht']].append(visitor_data['visitor_num'])

    # Sum by month
    visitors_purpose_sum = (visitors_purpose
                            .values('report_month')
                            .annotate(Sum('visitor_num'))
                            )

    json_obj = {}
    series = []

    series.append({'name': '全部',
                   'data': [data['visitor_num__sum']
                            for data in visitors_purpose_sum]})

    for area_key, data_list in data_dict.items():
        series.append({'name': area_key, 'data': data_list})

    if area == '前五地區':
        title_area = area
    else:
        title_area = area + '地區'

    json_obj['series'] = series
    json_obj['categories'] = categories
    json_obj['title'] = ({'text': '2016' + title_area + '來臺' + purpose + '旅客人數',
                          'x': -150,
                          'fontFamily': 'Helvetica Neue'})
    # print(json.dumps(json_obj))
    return HttpResponse(json.dumps(json_obj))
