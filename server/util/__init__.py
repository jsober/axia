import json
from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, obj):
        data = json.dumps(obj) + "\n"
        super(JsonResponse, self).__init__(data, content_type='application/json')
