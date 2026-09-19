from catalog.models import AgeGroup

mapping = {
    1: [4],
    2: [6],
    3: [8, 9],
}

for old_id, new_ids in mapping.items():
    try:
        old = AgeGroup.objects.get(id=old_id)
    except AgeGroup.DoesNotExist:
        print(f"old id={old_id} not found, skipping")
        continue

    if old.description:
        for new_id in new_ids:
            try:
                new = AgeGroup.objects.get(id=new_id)
            except AgeGroup.DoesNotExist:
                print(f"new id={new_id} not found, skipping")
                continue
            if not new.description:
                new.description = old.description
                new.save()
                print(f"Copied description from id={old_id} to id={new_id}: {old.description}")
            else:
                print(f"id={new_id} already has a description, not overwritten")

deleted_ids = list(mapping.keys())
qs = AgeGroup.objects.filter(id__in=deleted_ids)
count = qs.count()
qs.delete()
print(f"Deleted {count} old duplicate age groups: {deleted_ids}")

print()
print("Remaining age groups:")
for g in AgeGroup.objects.all().order_by("min_age_months"):
    print(g.id, g.title, g.min_age_months, g.max_age_months, g.description)