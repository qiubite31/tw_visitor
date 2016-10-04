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


def get_detail_visitor_data(request, purpose, area):
    # retrieve the certain purpose data
    visitors_all = (ArrivalRecord.objects
                    .order_by('report_year', 'report_month')
                    .values('report_year', 'report_month', 'visitor_num',
                            'purpose_cht', 'area_cht')
                    )
    visitors = visitors_all.filter(purpose_cht=purpose)

    if not area == '前五地區':
        visitors_single_area = (visitors
                                .filter(area_cht=area)
                                .values('report_year', 'report_month',
                                        'visitor_num')
                                )
        visitors_single_area_year = (visitors
                                     .filter(area_cht=area)
                                     .values('report_year')
                                     .annotate(Sum('visitor_num'))
                                     .order_by('-visitor_num__sum')
                                     )
        data_dict = OrderedDict()
        data_dict_year = OrderedDict()
        # fetch monthly data
        for visitor in visitors_single_area:
            year = visitor['report_year']
            month = (str(visitor['report_month'])
                     if visitor['report_month']-10 >= 0
                     else '0' + str(visitor['report_month']))
            report_key = str(year) + '-' + str(month)
            visitor_data = {report_key: visitor['visitor_num']}
            data_dict.setdefault(area, []).append(visitor_data)
        # fetch yearly data
        for visitor in visitors_single_area_year:
            visitor_data = {visitor['report_year']: visitor['visitor_num__sum']}
            data_dict_year.setdefault(area, []).append(visitor_data)
    else:
        # get the top 5 area list
        visitors_area_sum = (visitors
                             .values('area_cht')
                             .annotate(Sum('visitor_num'))
                             .order_by('-visitor_num__sum')
                             )
        area_top5 = []
        for idx, data in enumerate(visitors_area_sum):
            if idx > 4:
                break
            area_top5.append(data['area_cht'])

        visitors_top5_area = visitors.filter(area_cht__in=area_top5)
        visitors_top5_area_year = (visitors
                                   .filter(area_cht__in=area_top5)
                                   .values('report_year', 'area_cht')
                                   .annotate(Sum('visitor_num'))
                                   .order_by('report_year'))

        data_dict = OrderedDict()
        data_dict_year = OrderedDict()
        # initial dict by top5 sequence
        for area_key in area_top5:
            data_dict[area_key] = []
            data_dict_year[area_key] = []

        for visitor in visitors_top5_area:
            year = visitor['report_year']
            month = (str(visitor['report_month'])
                     if visitor['report_month']-10 >= 0
                     else '0' + str(visitor['report_month']))
            report_key = str(year) + '-' + str(month)
            visitor_data = {report_key: visitor['visitor_num']}
            data_dict[visitor['area_cht']].append(visitor_data)

        for visitor in visitors_top5_area_year:
            visitor_data = {visitor['report_year']: visitor['visitor_num__sum']}
            data_dict_year[visitor['area_cht']].append(visitor_data)
        
        print(visitors_top5_area_year)

    # month total
    visitors_month_sum = (ArrivalRecord.objects
                          .values('report_year', 'report_month')
                          .filter(purpose_cht=purpose)
                          .annotate(Sum('visitor_num'))
                          )
    # year total
    visitors_year_sum = (ArrivalRecord.objects
                         .values('report_year')
                         .filter(purpose_cht=purpose)
                         .annotate(Sum('visitor_num'))
                         )
    json_obj = {}
    series = []
    categories = []
    series.append({'name': '全部',
                   'data': [data['visitor_num__sum']
                            for data in visitors_month_sum]})

    for area_key, data_list in data_dict.items():
        if not categories:
            categories = [list(value.keys())[0] for value in data_list]

        series.append({'name': area_key,
                       'data': [list(value.values())[0]
                                for value in data_list]})
    series_year = []
    categories_year = []
    series_year.append({'name': '全部',
                        'data': [data['visitor_num__sum']
                                 for data in visitors_year_sum]})

    for area_key, data_list in data_dict_year.items():
        if not categories_year:
            categories_year = [list(value.keys())[0] for value in data_list]

        series_year.append({'name': area_key,
                            'data': [list(value.values())[0]
                                     for value in data_list]})

    if area == '前五地區':
        title_area = area
    else:
        title_area = area + '地區'

    json_obj['series'] = series
    json_obj['categories'] = categories
    json_obj['title'] = ({'text': '2016' + title_area + '來臺' + purpose + '旅客人數',
                          'x': -150,
                          'fontFamily': 'Helvetica Neue'})
    json_obj['series_year'] = series_year
    json_obj['categories_year'] = categories_year
    # print(json.dumps(json_obj))
    return HttpResponse(json.dumps(json_obj))
