from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Visitor
from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg


def boken_test(request, month):
    from bokeh.plotting import figure, output_file, show, save

    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file
    output_file("visitors/static/visitors/bokeh_chart/lines.html")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)

    # show the results
    save(p)
    # return response

    from bokeh.plotting import figure
    from bokeh.embed import components

    plot = figure()
    plot.circle([1, 2], [3, 4])

    script, div = components(plot)
    context = {
        'script': script,
        'div': div
    }
    save(plot)
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

