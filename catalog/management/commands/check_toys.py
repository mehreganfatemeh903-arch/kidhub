import os
import requests
from django.core.management.base import BaseCommand
from catalog.models import Toy


class Command(BaseCommand):
    help = "Check that each Toy's image file exists on disk and its affiliate_url is reachable; list price_range."

    def handle(self, *args, **options):
        toys = Toy.objects.all().order_by("id")
        if not toys.exists():
            self.stdout.write(self.style.WARNING("No toys found in the database."))
            return

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        }

        for toy in toys:
            self.stdout.write("=" * 60)
            self.stdout.write(f"ID {toy.id}: {toy.title}")

            # --- Image check ---
            if toy.image:
                try:
                    image_path = toy.image.path
                except ValueError:
                    image_path = None

                if image_path and os.path.exists(image_path):
                    size = os.path.getsize(image_path)
                    if size > 0:
                        self.stdout.write(self.style.SUCCESS(
                            f"  [OK] Image exists: {toy.image.name} ({size} bytes)"
                        ))
                    else:
                        self.stdout.write(self.style.ERROR(
                            f"  [FAIL] Image file is empty: {toy.image.name}"
                        ))
                else:
                    self.stdout.write(self.style.ERROR(
                        f"  [FAIL] Image file missing on disk: {toy.image.name}"
                    ))
            else:
                self.stdout.write(self.style.ERROR("  [FAIL] No image set for this toy"))

            # --- Affiliate URL check ---
            if toy.affiliate_url:
                try:
                    resp = requests.get(
                        toy.affiliate_url, headers=headers, timeout=10, allow_redirects=True
                    )
                    if resp.status_code == 200:
                        self.stdout.write(self.style.SUCCESS(
                            f"  [OK] Link responds 200: {toy.affiliate_url}"
                        ))
                    else:
                        self.stdout.write(self.style.ERROR(
                            f"  [FAIL] Link status {resp.status_code}: {toy.affiliate_url}"
                        ))
                except requests.RequestException as e:
                    self.stdout.write(self.style.ERROR(
                        f"  [FAIL] Link error ({e}): {toy.affiliate_url}"
                    ))
            else:
                self.stdout.write(self.style.ERROR("  [FAIL] No affiliate_url set"))

            # --- Price ---
            if toy.price_range:
                self.stdout.write(f"  Price range: {toy.price_range}")
            else:
                self.stdout.write(self.style.WARNING("  [WARN] No price_range set"))

        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("Done."))
