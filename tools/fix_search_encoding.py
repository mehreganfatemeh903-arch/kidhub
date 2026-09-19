from pathlib import Path
import re

p = Path(r".\templates\catalog\search.html")
s = p.read_text(encoding="utf-8-sig")

marks = set("\u0637\u0638\u00e2\u00ef\u00a9\u00f0\u009f\u2019\u2020\u0152\u0153")
changed = 0

def fix(m):
    global changed
    t = m.group()
    if not any(c in t for c in marks):
        return t
    try:
        z = t.encode("cp1256").decode("utf-8")
    except UnicodeError:
        return t
    old_score = sum(c in marks for c in t)
    new_score = sum(c in marks for c in z)
    if new_score < old_score:
        changed += 1
        return z
    return t

s = re.sub(r"\S+", fix, s)
p.write_text(s, encoding="utf-8")
print("CHANGED=", changed)
