import json

from django.db import transaction
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from vo.nav.models import IonStorm, Obstacle
from vo.nav.forms import IonStormForm
from vo.util.info import short_system_name, SYSTEM_NAMES
from vo.util.nav import Point, Sector, navigate
from vo.util import JsonResponse


@require_http_methods(['POST'])
@transaction.commit_on_success
def sector_report(request):
    try:
        data = json.loads(request.POST['data'])
    except:
        return HttpResponseBadRequest('Missing or invalid JSON in POST data')

    form = IonStormForm(data)
    if form.is_valid():
        if data['has_storm']:
            storm, created = IonStorm.objects.get_or_create(**form.cleaned_data)
            storm.save()
        else:
            try:
                storm = IonStorm.objects.get(**form.cleaned_data)
                storm.delete()
            except IonStorm.DoesNotExist:
                pass

        if data['has_obstacles']:
            obstacle, created = Obstacle.objects.get_or_create(**form.cleaned_data)
            obstacle.save()
        else:
            try:
                obstacle = Obstacle.objects.get(**form.cleaned_data)
                obstacle.delete()
            except Obstacle.DoesNotExist:
                pass

        result = {'result': 'success'}
    else:
        errors = dict()
        for field in form:
            if field.errors:
                errors[field] = field.errors

        result = {'result': 'failure', 'errors': errors}

    return JsonResponse(result)


@require_http_methods(['GET'])
def plot(request):
    try:
        data = json.loads(request.GET['data'])
    except:
        return HttpResponseBadRequest('Missing or invalid JSON in POST data')

    strategy = 'safe'

    if isinstance(data, dict):
        route = data['route']
        if 'strategy' in data:
            strategy = data['strategy']
    else:
        route = data

    print 'STRATEGY:', strategy

    def sector(s, x, y):
        point = Point(x, y)
        system = short_system_name(SYSTEM_NAMES[s])
        return Sector(system, point)

    avoid = IonStorm.objects.sectors()
    obstacles = set()

    if strategy == 'safe':
        obstacles = set(Obstacle.objects.sectors())
        avoid = avoid | obstacles

    waypoints = [sector(*s) for s in route]
    steps = navigate(waypoints, avoid, obstacles)

    if steps:
        sectors = [s.sector_id() for s in steps]
        return JsonResponse({'result': 'success', 'route': sectors})
    else:
        return JsonResponse({'result': 'failure', 'error': 'No possible route found'})


@require_http_methods(['GET'])
def list_storms(request):
    storms = IonStorm.objects.sectors()
    sectors = [s.sector_id() for s in storms]
    sectors.sort()
    return JsonResponse({'result': 'success', 'storms': sectors})
