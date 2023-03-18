from django.core.management.base import BaseCommand
from graphene_crud_maker.core import CrudMaker


class Command(BaseCommand):
    help = "Create Graphene CRUD"


    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--name", type=str, required=True, help="App name to create the CRUD graphQL"
        )
        parser.add_argument(
            "-e",
            "--exclude",
            nargs="*",
            type=str,
            default=[],
            help="Fields to exclude in the CRUD (id, createdAt, updatedAt)",
        )

    def handle(self, *args, **options):
        name = options["name"]
        exclude = options["exclude"]
        CrudMaker(app_name=name, exclude_fields=exclude)
