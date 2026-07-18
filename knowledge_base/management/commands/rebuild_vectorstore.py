from django.core.management.base import BaseCommand
from knowledge_base.rag import rebuild_vector_store_from_all_docs

class Command(BaseCommand):
    help = 'Rebuilds the FAISS vectorstore from all documents in the database.'

    def handle(self, *args, **options):
        self.stdout.write("Starting vectorstore rebuild...")
        try:
            db = rebuild_vector_store_from_all_docs()
            if db:
                self.stdout.write(self.style.SUCCESS("Successfully rebuilt vectorstore from all documents!"))
            else:
                self.stdout.write(self.style.WARNING("No documents found or no chunks were extracted. Vectorstore is empty."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error rebuilding vectorstore: {e}"))
