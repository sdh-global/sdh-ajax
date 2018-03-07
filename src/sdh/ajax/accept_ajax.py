from __future__ import unicode_literals

import sys
import json
import logging

from django.http.response import HttpResponseBase, HttpResponse

try:
    from django.http.response import JsonResponse
except ImportError:
    class JsonResponse(HttpResponse):
        def __init__(self, data, **kwargs):
            kwargs.setdefault('content_type', 'application/json')
            dumps_params = kwargs.pop('json_dumps_params', {})
            data = json.dumps(data, **dumps_params)
            super(JsonResponse, self).__init__(content=data, **kwargs)

from django.http import Http404
from django.conf import settings
from django.views.debug import ExceptionReporter
from django.contrib import messages

logger = logging.getLogger('django.request')


def accept_ajax(view_func):
    def _wrap_view_func(request, *args, **kwargs):
        try:
            response = view_func(request, *args, **kwargs)
        except Http404 as e:
            raise Http404(e)

        except Exception:
            if not request.is_ajax():
                raise

            logger.error('Internal Server Error: %s' % request.path,
                         exc_info=sys.exc_info(),
                         extra={'status_code': 500,
                                'request': request}
                         )
            response = {'status_code': 500,
                        'extension': 'sdh.ajax.accept_ajax',
                        'request_path': request.path}
            if settings.DEBUG:
                report = ExceptionReporter(request, *sys.exc_info())
                response['debug_msg'] = report.get_traceback_text()
                response['debug_html'] = report.get_traceback_html()
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

        resp = {'status_code': 200,
                'headers': [],
                'extension': 'sdh.ajax.accept_ajax'}

        message_list = []
        # compatibility with jquery-django-messages-ui
        for message in messages.get_messages(request):
            message_list.append({
                    "level": message.level,
                    "message": message.message,
                    "tags": message.tags,
                    })
        if message_list:
            resp['messages'] = message_list

        non_ajax_handler = None
        if isinstance(response, dict):
            resp['content'] = response
            resp['type'] = 'dict'
            non_ajax_handler = JsonResponse

        elif isinstance(response, (list, tuple)):
            resp['content'] = response
            resp['type'] = 'list'
            non_ajax_handler = JsonResponse

        elif isinstance(response, HttpResponseBase) and response['Content-Type'] == 'application/json':
            return response
        elif isinstance(response, HttpResponseBase) and request.is_ajax() and response.status_code in (301, 302):
            resp['status_code'] = response.status_code
            resp['type'] = 'redirect'
            resp['headers'] = {'location': response.get('location')}
            return JsonResponse(resp, json_dumps_params={'ensure_ascii': False})
        else:
            resp['content'] = response.content
            resp['type'] = 'string'
            resp['headers'] = response._headers

        if request.is_ajax() or non_ajax_handler:
            new_response = JsonResponse(resp, json_dumps_params={'ensure_ascii': False})
        else:
            new_response = response

        return new_response

    return _wrap_view_func
