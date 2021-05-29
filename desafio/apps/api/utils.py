import base64
import json
from importlib import import_module

import coreapi
from coreapi.codecs.corejson import _document_to_primitive, force_bytes
from coreapi.compat import COMPACT_SEPARATORS, VERBOSE_SEPARATORS

from rest_framework.documentation import (
    SchemaGenerator, SchemaJSRenderer as SchemaJSRenderBase, api_settings,
    get_docs_view, get_schema_view,
)
from rest_framework.pagination import PageNumberPagination

from django.apps import apps
from django.conf.urls import url
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.template import loader
from django.urls import include, path
from django.utils.encoding import force_text
from django.utils.functional import Promise
from django.utils.html import mark_safe

get_schema_js_view_parameters_dict = {
    'title': None,
    'description': None,
    'schema_url': None,
    'urlconf': None,
    'public': True,
    'patterns': None,
    'generator_class': SchemaGenerator,
    'authentication_classes': api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    'permission_classes': api_settings.DEFAULT_PERMISSION_CLASSES,
}
include_docs_urls_parameters_dict = {
    'title': None,
    'description': None,
    'schema_url': None,
    'urlconf': None,
    'public': True,
    'patterns': None,
    'generator_class': SchemaGenerator,
    'authentication_classes': api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    'permission_classes': api_settings.DEFAULT_PERMISSION_CLASSES,
    'renderer_classes': None
}


def include_api_urls(version, namespace):
    includes = []

    for app in apps.get_app_configs():
        try:
            urlconf_module = import_module(f'{app.name}.urls')
            if hasattr(urlconf_module, f'{version}_api_urlpatterns'):
                patterns = getattr(urlconf_module, f'{version}_api_urlpatterns')
            else:
                patterns = None
        except ModuleNotFoundError:
            pass
        else:
            if patterns:
                prefix = getattr(urlconf_module, 'app_api_prefix', app.name)
                if prefix:
                    prefix += '/'
                includes.append(
                    path(f'{prefix}api/{version}/', include((patterns, app.name), namespace=app.name))
                )

    return include((includes, namespace), namespace)


class FilterPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return JsonResponse({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


class CustomJSONCodec(coreapi.codecs.CoreJSONCodec):
    def encode(self, document, **options):
        """
        Takes a document and returns a bytestring.
        """
        indent = options.get('indent')

        if indent:
            kwargs = {
                'ensure_ascii': False,
                'indent': 4,
                'separators': VERBOSE_SEPARATORS,
                'cls': LazyEncoder
            }
        else:
            kwargs = {
                'ensure_ascii': False,
                'indent': None,
                'separators': COMPACT_SEPARATORS,
                'cls': LazyEncoder
            }

        data = _document_to_primitive(document)
        return force_bytes(json.dumps(data, **kwargs))


class SchemaJSRenderer(SchemaJSRenderBase):
    media_type = 'application/javascript'
    format = 'javascript'
    charset = 'utf-8'
    template = 'rest_framework/schema.js'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        codec = CustomJSONCodec()
        schema = base64.b64encode(codec.encode(data)).decode('ascii')

        template = loader.get_template(self.template)
        context = {'schema': mark_safe(schema)}
        request = renderer_context['request']
        return template.render(context, request=request)


def get_schemajs_view(get_schema_js_view_parameters: get_schema_js_view_parameters_dict):
    args = get_schema_js_view_parameters_dict
    args.update(get_schema_js_view_parameters)
    renderer_classes = [SchemaJSRenderer]

    return get_schema_view(
        title=args['title'],
        url=args['schema_url'],
        urlconf=args['urlconf'],
        description=args['description'],
        renderer_classes=renderer_classes,
        public=args['public'],
        patterns=args['patterns'],
        generator_class=args['generator_class'],
        authentication_classes=args['authentication_classes'],
        permission_classes=args['permission_classes'],
    )


def include_docs_urls(include_docs_urls_parameters: include_docs_urls_parameters_dict):
    args = include_docs_urls_parameters_dict
    args.update(include_docs_urls_parameters)

    docs_view = get_docs_view(
        title=args['title'],
        description=args['description'],
        schema_url=args['schema_url'],
        urlconf=args['urlconf'],
        public=args['public'],
        patterns=args['patterns'],
        generator_class=args['generator_class'],
        authentication_classes=args['authentication_classes'],
        renderer_classes=args['renderer_classes'],
        permission_classes=args['permission_classes'],
    )

    get_schema_js_view_parameters = {
        'title': args['title'],
        'description': args['description'],
        'schema_url': args['schema_url'],
        'urlconf': args['urlconf'],
        'public': args['public'],
        'patterns': args['patterns'],
        'generator_class': args['generator_class'],
        'authentication_classes': args['authentication_classes'],
        'permission_classes': args['permission_classes'],
    }
    schema_js_view = get_schemajs_view(get_schema_js_view_parameters)

    urls = [
        url(r'^$', docs_view, name='docs-index'),
        url(r'^schema.js$', schema_js_view, name='schema-js')
    ]
    return include((urls, 'api-docs'), namespace='api-docs')
