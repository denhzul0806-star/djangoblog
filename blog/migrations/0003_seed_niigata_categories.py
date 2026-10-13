from django.db import migrations


CATEGORIES = [
    "Travel Around Niigata",
    "Niigata Station Izakaya",
    "Food",
    "Restaurant",
]


def create_categories(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    for name in CATEGORIES:
        Category.objects.get_or_create(name=name)


def remove_categories(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    Category.objects.filter(name__in=CATEGORIES).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_tag_post_tags"),
    ]   

    operations = [
        migrations.RunPython(create_categories, remove_categories),
    ]
