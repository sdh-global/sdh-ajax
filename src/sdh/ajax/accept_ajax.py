import sys
import logging
import functools

from django.http.response import HttpResponseBase
from django.http.response import JsonResponse
from django.db import connections

from django.http import Http404
from django.conf import settings
from django.views.debug import ExceptionReporter
from django.contrib import messages

logger_name = getattr(settings, 'SDH_AJAX_LOGGER', 'django.request')
logger = logging.getLogger(logger_name)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def accept_ajax(view_func):
    @functools.wraps(view_func)
    def _wrap_view_func(request, *args, **kwargs):
        try:
            response = view_func(request, *args, **kwargs)
        except Http404 as e:
            raise Http404(e)

        except Exception:
            if not is_ajax(request):
                raise

            for db in connections.all():
                if db.settings_dict['ATOMIC_REQUESTS'] and db.in_atomic_block:
                    db.set_rollback(True)

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

        elif isinstance(response, HttpResponseBase) and is_ajax(request) and response.status_code in (301, 302):
            resp['status_code'] = response.status_code
            resp['type'] = 'redirect'
            resp['headers'] = {'location': response.get('location')}
            return JsonResponse(resp, json_dumps_params={'ensure_ascii': False})

        elif isinstance(response, HttpResponseBase) and is_ajax(request):
            # do processing only if request is ajax
            buff = response.content
            if isinstance(buff, bytes):
                buff = buff.decode('utf-8')
            resp['content'] = buff
            resp['type'] = 'string'
            resp['headers'] = dict(getattr(response, '_headers', {}) or getattr(response, 'headers', {}))

        if is_ajax(request) or non_ajax_handler:
            new_response = JsonResponse(resp, json_dumps_params={'ensure_ascii': False})
        else:
            new_response = response

        return new_response

    return _wrap_view_func
