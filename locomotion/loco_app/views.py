import json

from django.forms import (
    Form, ModelMultipleChoiceField, MultipleChoiceField, DateField
)
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Filials, Mileage

class LocoForm(Form):

    filial = ModelMultipleChoiceField(
        Filials.objects.all(), required=False
    )
    serie = MultipleChoiceField(
        choices=[(x, '_') for x in
            Mileage.objects.distinct(
                'serie_name'
            ).values_list('serie_name', flat=True)],
        required=False
    )
    date_from = DateField(required=False)
    date_to = DateField(required=False)

# Create your views here.
@ensure_csrf_cookie
def index_view(request):

    filials = Filials.objects.all()
    series = set()
    filial_series = {}
    for r in  Mileage.objects.all().select_related('filial'):
        series.add(r.serie_name)
        filial_series.setdefault(
            r.filial_id, set()
        ).add(r.serie_name)
    for f, s in filial_series.items():
        filial_series[f] = list(s)
    return render(request, 'loco_app/templates/index.html', {
        'filials': filials,
        'series': sorted(series),
        'filial_series': filial_series
    })

@require_GET
def json_view(request):
    if not request.is_ajax():
        raise Http404

    form = LocoForm(request.GET or None)
    if not form.is_valid():
        return HttpResponseBadRequest(
            form.errors.as_json(), content_type='text/javascript'
        )
    result = Mileage.objects.chart_data(**form.cleaned_data)
    return HttpResponse(json.dumps(result), content_type='text/javascript')
