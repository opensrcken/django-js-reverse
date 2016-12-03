# -*- coding: utf-8 -*-
import sys

from django.conf import settings
from django.core import urlresolvers
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand
from django_js_reverse.core import generate_ts


class Command(BaseCommand):
    help = 'Creates a Typescript interface file for django-js-reverse'

    def get_location(self):
        output_path = getattr(settings, 'JS_REVERSE_TS_OUTPUT_PATH', None)
        if output_path:
            return output_path
        raise ImproperlyConfigured(
            'The generate_js_reverse_ts_interfaces command needs settings.JS_REVERSE_TS_OUTPUT_PATH to be set.')

    def handle(self, *args, **options):
        location = self.get_location()
        file = 'django-urls.ts'
        fs = FileSystemStorage(location = location)
        if fs.exists(file):
            fs.delete(file)

        default_urlresolver = urlresolvers.get_resolver(None)
        content = generate_ts(default_urlresolver)
        fs.save(file, ContentFile(content))
        if len(sys.argv) > 1 and sys.argv[1] in ['generate_js_reverse_ts_interfaces']:
            self.stdout.write('django-urls.ts file written to %s' % (location))  # pragma: no cover
