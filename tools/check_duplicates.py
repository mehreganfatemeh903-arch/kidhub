from catalog.models import AgeGroup
from collections import defaultdict

fields = [f.name for f in AgeGroup._meta.fields if f.name != "id"]
print("FIELDS:", fields)
print()

all_groups = AgeGroup.objects.all().order_by("id")
for g in all_groups:
    vals = {f: getattr(g, f) for f in fields}
    print(g.id, vals)

print()
print("EXACT DUPLICATES (identical values across all fields):")
groups = defaultdict(list)
for g in all_groups:
    key = tuple(getattr(g, f) for f in fields)
    groups[key].append(g.id)

found = False
for key, ids in groups.items():
    if len(ids) > 1:
        found = True
        print(key, "-> ids:", ids)

if not found:
    print("No exact duplicates found by field values. Check the printed list above manually for overlapping age ranges with different labels.")