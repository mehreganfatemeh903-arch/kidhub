from datetime import date

from catalog.models import AgeGroup, Toy, Book


def calculate_age_months(birth_date: date, today: date | None = None) -> int:
    today = today or date.today()
    months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)

    if today.day < birth_date.day:
        months -= 1

    return max(months, 0)


def normalize_text(value: str) -> str:
    return " ".join(str(value or "").lower().strip().split())


GOAL_TO_DEVELOPMENT_AREAS = {
    "مهارت حرکتی": {
        "حرکتی ظریف",
        "حرکتی درشت",
        "مهارت حرکتی ظریف",
        "مهارت حرکتی درشت",
        "هماهنگی چشم و دست",
        "هماهنگی",
        "دست‌ورزی",
        "آمادگی نوشتن",
    },
    "مهارت اجتماعی": {
        "اجتماعی",
        "مهارت اجتماعی",
        "مهارت‌های اجتماعی و ارتباطی",
        "مهارت‌های اجتماعی و رفتاری",
        "ارتباط",
        "تعامل",
        "همکاری",
        "دوستی",
        "خانواده",
        "احساسات",
        "آداب اجتماعی",
        "رفتار",
        "مرزهای شخصی",
        "مالکیت",
        "مسئولیت",
    },
    "خلاقیت": {
        "خلاقیت",
        "هنری",
        "تصور",
        "بیان تصویری",
    },
    "یادگیری": {
        "شناخت",
        "شناختی",
        "زبان",
        "واژگان",
        "دانش",
        "دانش علمی",
        "دانش عمومی",
        "حل مسئله",
        "تفکر",
        "ریاضی",
        "کنجکاوی",
        "پرسشگری",
        "مشاهده",
        "یادگیری",
        "آگاهی زبانی",
        "آمادگی خواندن",
    },
    "تمرکز": {
        "تمرکز",
        "تمرکز و توجه",
        "توجه",
        "حل مسئله",
        "مشاهده",
        "انتظار",
        "تشخیص الگو",
        "کنجکاوی",
    },
}


def get_goal_area_matches(goals, development_names):
    areas = set(development_names)
    return [
        goal
        for goal in goals
        if areas.intersection(GOAL_TO_DEVELOPMENT_AREAS.get(goal, set()))
    ]


def interest_matches(interests, searchable_text):
    return [
        interest
        for interest in interests
        if len(interest) >= 3 and interest in searchable_text
    ]


def score_item(
    *,
    age_match,
    goal_matches,
    interest_matches_list,
    strong_text_matches=0,
):
    score = 0
    reasons = []

    if age_match:
        score += 40
        reasons.append("مناسب سن کودک")

    goal_count = min(len(goal_matches), 2)
    if goal_count:
        score += goal_count * 15
        reasons.append(
            f"هماهنگ با {goal_count} هدف رشد کودک"
        )

    interest_count = min(len(interest_matches_list), 2)
    if interest_count:
        score += interest_count * 10
        reasons.append(
            f"مرتبط با {interest_count} علاقه کودک"
        )

    if strong_text_matches:
        score += min(strong_text_matches * 5, 10)
        reasons.append("تطابق محتوایی قوی")

    return min(score, 100), reasons
def recommend_for_child(child, limit: int = 5):
    age_months = calculate_age_months(child.birth_date)

    interests = [
        normalize_text(item)
        for item in (child.interests or [])
        if isinstance(item, str) and item.strip()
    ]

    goals = [
        normalize_text(item)
        for item in (child.goals or [])
        if isinstance(item, str) and item.strip()
    ]

    age_group_ids = list(
        AgeGroup.objects.filter(
            min_age_months__lte=age_months,
            max_age_months__gte=age_months,
        ).values_list("id", flat=True)
    )

    results = []

    for toy in Toy.objects.prefetch_related(
        "age_groups",
        "development_areas",
    ):
        age_match = toy.age_groups.filter(
            id__in=age_group_ids
        ).exists()

        development_names = [
            normalize_text(area.name)
            for area in toy.development_areas.all()
        ]

        matched_goals = get_goal_area_matches(
            goals,
            development_names,
        )

        searchable_text = normalize_text(
            " ".join([
                toy.title,
                toy.short_description,
                toy.why_it_helps,
                *development_names,
            ])
        )

        matched_interests = interest_matches(
            interests,
            searchable_text,
        )

        strong_matches = sum(
            1
            for value in interests + goals
            if value and value in searchable_text
        )

        score, reasons = score_item(
            age_match=age_match,
            goal_matches=matched_goals,
            interest_matches_list=matched_interests,
            strong_text_matches=strong_matches,
        )

        if score > 0:
            results.append({
                "type": "toy",
                "id": toy.id,
                "title": toy.title,
                "slug": toy.slug,
                "score": score,
                "match_reasons": reasons,
                "short_description": toy.short_description,
                "why_it_helps": toy.why_it_helps,
                "image": toy.image.url if toy.image else None,
                "price_range": toy.price_range,
                "affiliate_url": toy.affiliate_url,
            })

    for book in Book.objects.prefetch_related("age_groups"):
        age_match = book.age_groups.filter(
            id__in=age_group_ids
        ).exists()

        book_text = normalize_text(
            " ".join([
                book.title,
                book.description,
                book.topic or "",
                book.developmental_benefit or "",
            ])
        )

        book_development_text = normalize_text(
            " ".join([
                book.topic or "",
                book.developmental_benefit or "",
            ])
        )

        matched_goals = []

        for goal in goals:
            mapped = GOAL_TO_DEVELOPMENT_AREAS.get(goal, set())

            if any(area in book_development_text for area in mapped):
                matched_goals.append(goal)

        matched_interests = interest_matches(
            interests,
            book_text,
        )

        strong_matches = sum(
            1
            for value in interests + goals
            if value and value in book_text
        )

        score, reasons = score_item(
            age_match=age_match,
            goal_matches=matched_goals,
            interest_matches_list=matched_interests,
            strong_text_matches=strong_matches,
        )

        if score > 0:
            results.append({
                "type": "book",
                "id": book.id,
                "title": book.title,
                "slug": book.slug,
                "score": score,
                "match_reasons": reasons,
                "description": book.description,
                "book_type": book.book_type,
                "cover_image": (
                    book.cover_image.url
                    if book.cover_image
                    else None
                ),
                "source_name": book.source_name,
                "source_url": book.source_url,
            })

    results.sort(
        key=lambda item: (
            -item["score"],
            item["type"] != "toy",
            item["title"],
        )
    )

    return {
        "child": {
            "id": child.id,
            "name": child.name,
        },
        "age_months": age_months,
        "recommendations": (
            [item for item in results if item["type"] == "toy"][:3]
            + [item for item in results if item["type"] == "book"][:2]
        )[:limit],
    }
