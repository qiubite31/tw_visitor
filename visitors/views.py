from django.shortcuts import render, get_object_or_404
from .models import Visitor


def index(request):
    return render(request, 'visitors/index.html', {})


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

