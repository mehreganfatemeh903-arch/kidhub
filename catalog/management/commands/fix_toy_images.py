import os
import re
from django.core.management.base import BaseCommand
from django.core.files import File
from catalog.models import Toy


class Command(BaseCommand):
    help = "Assign local image files (named toy-<id>.<ext>) from a staging folder to their matching Toy records."

    def add_arguments(self, parser):
        parser.add_argument("folder", type=str, help="Path to folder containing images named toy-<id>.jpg/png/webp")

    def handle(self, *args, **options):
        folder = options["folder"]
        if not os.path.isdir(folder):
            self.stdout.write(self.style.ERROR(f"Folder not found: {folder}"))
            return

        pattern = re.compile(r"^toy-(\d+)\.(jpg|jpeg|png|webp)$", re.IGNORECASE)
        matched = 0

        for filename in sorted(os.listdir(folder)):
            match = pattern.match(filename)
            if not match:
                continue

            toy_id = int(match.group(1))
            try:
                toy = Toy.objects.get(id=toy_id)
            except Toy.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"No Toy with id={toy_id}, skipping {filename}"))
                continue

            full_path = os.path.join(folder, filename)
            with open(full_path, "rb") as f:
                toy.image.save(filename, File(f), save=True)

            self.stdout.write(self.style.SUCCESS(f"Assigned {filename} -> Toy id={toy_id} ({toy.title})"))
            matched += 1

        self.stdout.write(self.style.SUCCESS(f"Done. {matched} images assigned."))
