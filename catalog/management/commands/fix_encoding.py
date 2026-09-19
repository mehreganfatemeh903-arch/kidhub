import re
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models

UNICODE_ESCAPE_PATTERN = re.compile(r"\\u[0-9a-fA-F]{4}")
TARGET_MODELS = ["Toy", "Book", "Article", "Lullaby", "AgeGroup", "DevelopmentArea", "AffiliateSource"]


class Command(BaseCommand):
    help = "Detect and fix text fields containing literal \\uXXXX escape sequences instead of real Unicode text."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Preview changes without saving.")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        app_config = apps.get_app_config("catalog")
        total_fixed = 0

        for model_name in TARGET_MODELS:
            try:
                model = app_config.get_model(model_name)
            except LookupError:
                continue

            text_fields = [
                f.name for f in model._meta.get_fields()
                if isinstance(f, (models.CharField, models.TextField))
            ]

            for obj in model.objects.all():
                changed = False
                for field_name in text_fields:
                    value = getattr(obj, field_name, None)
                    if isinstance(value, str) and UNICODE_ESCAPE_PATTERN.search(value):
                        try:
                            fixed_value = value.encode("ascii").decode("unicode_escape")
                        except (UnicodeDecodeError, UnicodeEncodeError):
                            continue

                        self.stdout.write(f"{model_name} id={obj.pk} field={field_name}")
                        self.stdout.write(f"  BEFORE: {value}")
                        self.stdout.write(f"  AFTER : {fixed_value}")
                        setattr(obj, field_name, fixed_value)
                        changed = True

                if changed:
                    total_fixed += 1
                    if not dry_run:
                        obj.save()

        if dry_run:
            self.stdout.write(self.style.WARNING(f"[DRY RUN] {total_fixed} records would be fixed. Nothing saved."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Fixed {total_fixed} records."))
