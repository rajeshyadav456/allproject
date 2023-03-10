from django.core.management.base import BaseCommand

from soteria.roles.helper import sync_org_users_permissions


class Command(BaseCommand):
    help = "Sync the roles and their permissions for organization members"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        sync_org_users_permissions()
        self.stdout.write(self.style.SUCCESS(f"Successfully synced all organization members roles"))
