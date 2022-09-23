from django.core.management.base import BaseCommand
from csv import DictReader

from users.models import User
from reviews.models import Review, Comment

CSV_ROOT = "static/data/"
CSV_MODEL = {
    "users.csv": User,
    "review.csv": Review,
    "comments.csv": Comment,
}
FK_VALUE = {"author": User, "review_id": Review}


class Command(BaseCommand):
    help = "Импорт данных из scv"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_name",
            help=(
                "Enter the csv-file names to import.\n"
                "Format: users.csv\n\n"
                "Or nothing to import all."
            ),
            nargs="*",
            default="all",
        )

    def handle(self, *args, **options):
        def importer(csv_name):
            url = CSV_ROOT + csv_name
            for row in DictReader(open(url, encoding="utf-8")):
                model = CSV_MODEL[csv_name]
                model_kwargs = {}
                for field in model._meta.get_fields():
                    name = field.name
                    name_id = name + '_id'
                    if name in row or name_id in row:
                        if name in FK_VALUE:
                            fobject = FK_VALUE[name].objects.get(
                                id=row[name]
                            )
                            model_kwargs[name] = fobject
                        elif name_id in FK_VALUE:
                            fobject = FK_VALUE[name_id].objects.get(
                                id=row[name_id]
                            )
                            model_kwargs[name] = fobject
                        else:
                            model_kwargs[name] = row[name]
                object = model(**model_kwargs)
                object.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully imported file "%s"' % csv_name
                )
            )

        if options["csv_name"] == "all":
            for csv_name in CSV_MODEL.keys():
                importer(csv_name)
        else:
            for csv_name in options["csv_name"]:
                if csv_name not in CSV_MODEL.keys():
                    raise KeyError('"%s"| Неизвестное имя файла' % csv_name)
                importer(csv_name)
