import json

from django.db import transaction
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from vo.econ.forms import StationForm, FactionForm, ItemForm, SaleItemForm
from vo.econ.models import Station, Faction, Item, SaleItem
from vo.util import JsonResponse
from vo.util.nav import shortest_jump_plans
from vo.util.info import SYSTEM_NAMES, short_system_name


def validation_error_response(label, form):
    errors = dict()
    for field in form:
        if field.errors:
            errors[field.name] = field.errors

    return JsonResponse({'result': 'failure', 'label': label, 'errors': errors})


@require_http_methods(['POST'])
@transaction.commit_on_success
def station_report(request):
    try:
        data = json.loads(request.POST['data'])
    except:
        return HttpResponseBadRequest('Missing or invalid JSON in POST data')

    # Save faction
    faction_form = FactionForm(data)
    if not faction_form.is_valid():
        return validation_error_response('Faction', faction_form)

    faction, created = Faction.objects.get_or_create(**faction_form.cleaned_data)

    # Save station
    station_form = StationForm(data)
    if not station_form.is_valid():
        return validation_error_response('Station', station_form)

    station, created = Station.objects.get_or_create(faction=faction, **station_form.cleaned_data)

    # Save each item and sale item for the station
    for item_data in data['items']:
        # Create a label for errors in this item's data
        label = 'Item'
        if 'item_name' in item_data and item_data['item_name']:
            label = item_data['item_name']

        item_form = ItemForm(item_data)
        if not item_form.is_valid():
            return validation_error_response(label, item_form)

        item, created = Item.objects.get_or_create(**item_form.cleaned_data)

        sale_form = SaleItemForm(item_data)
        if not sale_form.is_valid():
            return validation_error_response(label, sale_form)

        sale, created = SaleItem.objects.get_or_create(item=item, station=station, **sale_form.cleaned_data)

    return JsonResponse({'result': 'success'})


def sale_locations(data):
    if 'item' not in data:
        raise ValueError('Missing "item"')

    item = Item.objects.filter(item_name__iexact=data['item'])
    if not item:
        raise ValueError('Item not found')

    return SaleItem.objects.filter(item__in=item)


@require_http_methods(['GET'])
def nearest_sale_locations(request):
    try:
        data = json.loads(request.GET['data'])
    except:
        return HttpResponseBadRequest('Missing or invalid JSON in POST data')

    try:
        start = short_system_name(SYSTEM_NAMES[data['sid']])
    except:
        return JsonResponse({'result': 'failure', 'error': 'Start system not found'})

    try:
        sales = sale_locations(data)
    except ValueError, e:
        return JsonResponse({'result': 'failure', 'error': str(e)})

    min_hops = None
    results = []

    for sale in sales:
        plans = shortest_jump_plans(start, sale.station.short_system())
        hops = len(plans[0])

        if min_hops is None or hops < min_hops:
            min_hops = hops
            results = [sale]
        elif hops == min_hops:
            results.append(sale)

    results = sorted(results, key=lambda r: r.price)

    return JsonResponse({
        'result': 'success',
        'locations': [str(s) for s in results],
    })


@require_http_methods(['GET'])
def cheapest_sale_locations(request):
    try:
        data = json.loads(request.GET['data'])
    except:
        return HttpResponseBadRequest('Missing or invalid JSON in POST data')

    try:
        sales = sale_locations(data)
    except ValueError, e:
        return JsonResponse({'result': 'failure', 'error': str(e)})

    sales = sales.order_by('price')

    return JsonResponse({
        'result': 'success',
        'locations': [str(s) for s in sales[:6]],
    })
