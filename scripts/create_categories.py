# scripts/create_categories.py
# It will create categories

from discussion.models import Category  # adjust to your actual Category model path

CATEGORIES = [
    "Technology",
    "Finance & Jobs",
    "Health & Fitness",
    "Relationships & Emotions",
    "Religion & Spirituality",
    "Self-Improvement",
    "Food & Travel",
    "Education & Career",
    "Entertainment & Media",
    "Parenting & Pets",
    "Lifestyle",
    "General Questions",
    "Other",
]

def run():
    for title in CATEGORIES:
        Category.objects.get_or_create(title=name)
