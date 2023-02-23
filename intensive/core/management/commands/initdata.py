from glob import glob

from django.core.exceptions import ImproperlyConfigured
from django.core.management import CommandError, call_command
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections


class Command(BaseCommand):
    help = "Populate database with initial data"
    requires_migrations_checks = False

    def handle(self, *args, **kwargs):
        is_migrations_good = self.check_migrations()
        if not is_migrations_good:
            return
        fixture_paths = glob("*/fixtures/*.json")
        call_command("loaddata", fixture_paths)
        try:
            # get creditinals froom env
            call_command(
                "createsuperuser", skip_checks=True, interactive=False
            )
        except CommandError:
            # else get from prompt
            call_command("createsuperuser", skip_checks=True)

    def check_migrations(self):
        """
        Print a warning if the set of migrations on disk don't match the
        migrations in the database.
        """
        from django.db.migrations.executor import MigrationExecutor

        try:
            executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
        except ImproperlyConfigured:
            # No databases are configured (or the dummy one)
            return

        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            apps_waiting_migration = sorted(
                {migration.app_label for migration, backwards in plan}
            )
            self.stdout.write(
                self.style.NOTICE(
                    "\nYou have %(unapplied_migration_count)s unapplied "
                    "migration(s). Your project may not work properly "
                    "until you apply the migrations for app(s): "
                    "%(apps_waiting_migration)s."
                    % {
                        "unapplied_migration_count": len(plan),
                        "apps_waiting_migration": ", ".join(
                            apps_waiting_migration
                        ),
                    }
                )
            )
            self.stdout.write(
                self.style.NOTICE(
                    "Run 'python manage.py migrate' to apply them."
                )
            )
            answer = None
            while not answer or answer not in "yn":
                answer = input("Do you wish to proceed? [yN] ")
                if not answer:
                    answer = "n"
                    break
                else:
                    answer = answer[0].lower()
            if answer != "y":
                return
        return True
