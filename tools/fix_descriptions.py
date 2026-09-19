import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kidhub.settings")
django.setup()

from catalog.models import AgeGroup

updates = {
    4: "رشد حرکتی 🏃",
    6: "رشد زبانی 🗣️",
    8: "خلاقیت 🎨",
    9: "خلاقیت 🎨",
}

for group_id, desc in updates.items():
    try:
        g = AgeGroup.objects.get(id=group_id)
    except AgeGroup.DoesNotExist:
        print(f"id={group_id} not found, skipping")
        continue

    if not g.description:
        g.description = desc
        g.save()
        print(f"Updated id={group_id} ({g.title}) -> {desc}")
    else:
        print(f"id={group_id} ({g.title}) already has description: {g.description}, not overwritten")

print()
print("Final list:")
for g in AgeGroup.objects.all().order_by("min_age_months"):
    print(g.id, g.title, g.min_age_months, g.max_age_months, g.description)