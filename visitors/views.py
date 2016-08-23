# encoding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ArrivalRecord
from django.db.models import Q
from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np


def show_highchart(request):
    return render(request, 'visitors/highchart.html', {'status': 'ok'})


def get_visitor_data(request, purpose, area):
    import json
    from django.db.models import Sum

    purpose_eng = purpose if purpose != 'All' else ''
    area_eng = area if purpose != 'All' else ''

    print(purpose_eng)
    print(area_eng)

    visitors_data = ArrivalRecord.objects.exclude(Q(purpose_cht='男') | Q(purpose_cht='女'))
    visitors_data_purpose = visitors_data.order_by('purpose_cht', 'report_month').values('purpose_cht', 'report_month')
    visitors_data_purpose = visitors_data_purpose.annotate(Sum('visitor_num'))

    if not purpose == 'All':
        visitors_data_purpose = visitors_data_purpose.filter(purpose_eng=purpose_eng)

    visitors_sum_data = visitors_data.order_by('report_month').values('report_month')
    visitors_sum_data = visitors_sum_data.annotate(Sum('visitor_num'))

    series_item = {}
    categories = set()
    for visitor_data in visitors_data_purpose:
        purpose = visitor_data['purpose_cht']
        month = visitor_data['report_month'] 
        number = visitor_data['visitor_num__sum']
        series_item.setdefault(purpose, []).append(number)
        categories.add(visitor_data['report_month'])

    series = []
    for name, data_list in series_item.items():
        series.append({'name': name, 'data': data_list})

    # print(visitors_sum_data)
    series.append({'name': '全部', 'data': [data['visitor_num__sum'] for data in visitors_sum_data]})
    # print(series)
    categories = list(categories)
    categories.sort()

    json_obj = {}
    json_obj['series'] = series
    json_obj['categories'] = categories
    # print(json.dumps(json_obj, indent=4))
    return HttpResponse(json.dumps(json_obj))


def get_area_data(request, area):
    import json
    visitors_data_by_area = ArrivalRecord.objects.filter(area_cht=area, purpose_cht='觀光').order_by('report_month').values()

    data_list = []
    categories = []
    for visitor_data in visitors_data_by_area:
        categories.append(visitor_data['report_month'])
        data_list.append(visitor_data['visitor_num'])

    json_obj = {}
    series = []
    series.append({'name': '大陸', 'data': data_list})  # , 'categories': categories}
    json_obj['series'] = series
    json_obj['categories'] = categories
    # json_obj.append(data_dict)
    print('大陸')
    print(json.dumps(json_obj, indent=4))
    return HttpResponse(json.dumps(json_obj))


def show_area_data(request, area):
    from bokeh.charts import Line
    from bokeh.embed import components
    import pandas as pd
    visitor_datas = ArrivalRecord.objects.values('area_cht')
    areas = set()
    for visitor_data in visitor_datas:
        areas.add(visitor_data['area_cht'])

    # visitors_data_by_area = ArrivalRecord.objects.filter(area_cht=area, purpose_cht='Pleasure').exclude(Q(purpose_cht='男') | Q(purpose_cht='女')).order_by('report_month').values()
    visitors_data_by_area = ArrivalRecord.objects.filter(area_cht=area, purpose_cht='觀光').order_by('report_month').values()
    visitor_df = pd.DataFrame.from_records(visitors_data_by_area)

    line = Line(visitor_df,
                x='report_month', y='visitor_num',
                ylabel='每月拜訪人次', xlabel='月份'
                )
    line.title = area + ' 地區來台觀光人次'
    script, div = components(line)

    context = {
        'areas': areas,
        'script': script,
        'div': div
    }
    return render(request, 'visitors/bokeh.html', context)


def boken_test(request, month):
    from bokeh.charts import Line, Bar, output_file, show, hplot
    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.models import OpenURL
    import pandas as pd
    import numpy as np

    from bokeh.models.widgets import Slider, Panel, Tabs, RadioButtonGroup
    from bokeh.io import vform
    radio_button_group = RadioButtonGroup(
        labels=["觀光 Pleasure", "會議 Conference", "Option 3"], active=1)

    # output_file("layout_widgets.html") , reason='觀光 Pleasure'
    visitors_data = Visitor.objects.filter(area='日本 Japan').exclude(Q(reason='男 Male') | Q(reason='女 Female')).order_by('report_month').values()
    visitor_df = pd.DataFrame.from_records(visitors_data)
    print(visitor_df)
    plot = Bar(visitor_df, 'reason', values='visitor_num', title='china visitor trend', group='report_month', legend='top_right')
    new_visitor_df = visitor_df.loc[visitor_df['reason'] == radio_button_group.labels[radio_button_group.active]]
    print(new_visitor_df)
    line = Line(new_visitor_df,
                x='report_month', y='visitor_num',
                ylabel='每月拜訪人次', xlabel='月份'
                )
    line.title = '日本地區來台觀光人次'
    # , plot_width=500, plot_height=400
    # plot.responsive = True
    layout = hplot(radio_button_group, line)
    script, div = components(layout)
    context = {
        'script': script,
        'div': div
    }
    return render(request, 'visitors/bokeh.html', context)


def plotResults(request, month):
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    import numpy as np
    # Prepare dataset
    visitors_by_month = Visitor.objects.filter(report_month=month)
    visitors_by_purpose = {}
    for visitor in visitors_by_month:
        if '男' in visitor.reason or '女' in visitor.reason:
            continue
        purpose = visitor.reason[visitor.reason.index(' ')+1:]
        visitor_num = visitor.visitor_num
        visitors_by_purpose.setdefault(purpose, visitor_num) + visitor_num
        """
        if purpose not in visitors_by_purpose.keys():
            visitors_by_purpose[purpose] = visitor_num
        else:
            visitors_by_purpose[purpose] = visitors_by_purpose[purpose] + visitor_num
        """
    visitors_by_purpose = sorted(visitors_by_purpose.items(), key=lambda x: x[1], reverse=True)
    print(visitors_by_purpose)
    reasons = [reason[0] for reason in visitors_by_purpose]
    visitor_num = [num[1] for num in visitors_by_purpose]

    N = len(reasons)
    ind = np.arange(N)  # x軸的組數量
    width = 0.5  # bar寬度

    cols = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'indigo']
    cols = cols[0:N]
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, visitor_num, width, color=cols)

    ax.set_title('2016-03 Taiwan Visitor Arrivals by Purpose of Visit')  # 圖表標題
    ax.set_ylabel('Visitor Number')
    ax.set_xlabel('Purpose')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(reasons)
    ax.legend(rects1, reasons)

    xtickNames = ax.set_xticklabels(reasons)
    plt.setp(xtickNames, rotation=45, fontsize=8)

    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def index(request):
    return render(request, 'visitors/index.html', test_matplotlib(request))


def visitor_reason(request, month):
    visitor_reasons = Visitor.objects.filter(report_month=month)
    visitor_reasons_distinct = set()
    for visitor in visitor_reasons:
        visitor_reasons_distinct.add(visitor.reason)
    context = {
        'visitor_reasons_distinct': visitor_reasons_distinct,
        'month': month,
    }
    return render(request, 'visitors/reason.html', context)


def visitor_detail(request, month, reason):
    visitor_record_by_reason = Visitor.objects.filter(report_month=month, reason=reason)
    context = {
        'visitor_record_by_reason': visitor_record_by_reason,
        'month': month
    }
    return render(request, 'visitors/detail.html', context)


def get_visitor(request, visitor_id):
    t = get_object_or_404(Visitor, pk=visitor_id)
    context = {
            'visitor': t,
        }
    return render(request, 'visitors/visitor.html', context)

