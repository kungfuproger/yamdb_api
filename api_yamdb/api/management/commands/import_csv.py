from django.core.management.base import BaseCommand
from csv import DictReader

from users.models import User
from reviews.models import Review, Comment

CSV_ROOT = "static/data/"
FILE_MODEL = {
    "users.csv": User,
    "review.csv": Review,
    "comments.csv": Comment,
}
FK_VALUE = {"author": User, "review_id": Review}


class Command(BaseCommand):
    help = "Импорт данных из scv"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            help=(
                "Enter the csv-file to import.\n"
                "Format: users.csv\n\n"
                "Or nothing to import all."
            ),
            nargs="*",
        )

    def handle(self, *args, **options):
        def importer(csv_file, model):
            url = CSV_ROOT + csv_file
            for row in DictReader(open(url, encoding="utf-8")):
                model_kwargs = {}
                for field in model._meta.get_fields():
                    name = field.name
                    name_id = name + "_id"
                    if name in row or name_id in row:
                        if name in FK_VALUE:
                            fkobject = FK_VALUE[name].objects.get(id=row[name])
                            model_kwargs[name] = fkobject
                        elif name_id in FK_VALUE:
                            fkobject = FK_VALUE[name_id].objects.get(
                                id=row[name_id]
                            )
                            model_kwargs[name] = fkobject
                        else:
                            model_kwargs[name] = row[name]
                object = model(**model_kwargs)
                object.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully imported file "%s"' % csv_file
                )
            )

        if options["csv_file"]:
            for csv_file in options["csv_file"]:
                if csv_file not in FILE_MODEL.keys():
                    raise KeyError('"%s"| Неизвестное имя файла' % csv_file)
                model = FILE_MODEL[csv_file]
                importer(csv_file, model)
        else:
            for csv_file, model in FILE_MODEL.items():
                importer(csv_file, model)
