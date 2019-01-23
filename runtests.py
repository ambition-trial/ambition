#!/usr/bin/env python
import django
import logging
import os
import sys

from django.test.runner import DiscoverRunner

APP_NAME = 'ambition_edc'


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ambition_edc.settings')
    django.setup()
    failures = DiscoverRunner(failfast=True).run_tests(
        [f'{APP_NAME}.tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
