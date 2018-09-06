
from django.core.management.base import BaseCommand

from ...permissions import PermissionsUpdater


class Command(BaseCommand):

    help = 'Update groups and group permissions'

    def handle(self, *args, **options):

        PermissionsUpdater()
