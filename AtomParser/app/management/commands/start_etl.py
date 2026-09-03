from django.core.management.base import BaseCommand

from etl_pipeline.ingest.django_orm import ingest

class Command(BaseCommand):
    help = "Parse enabled job sources and persist normalized jobs"

    def handle(self, *args, **options):
        self.stdout.write("Starting job ingestion...")

        ingest()

        self.stdout.write(
            self.style.SUCCESS("Job ingestion completed")
        )