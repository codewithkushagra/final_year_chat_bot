from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.utils.utils import SideBarSelectedMixin
from apps.ingest.tasks import ingest_data
from apps.ingest.models import Ingest


class IngestDataView(LoginRequiredMixin, SideBarSelectedMixin, generic.TemplateView):
    template_name = "pages/integrations/data_ingestion/data_ingestion.html"
    parent = "ingest"
    segment = "ingest_data"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent"] = self.parent
        context["segment"] = self.segment
        context["processes"] = Ingest.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        text_data = request.POST.get("text")
        file = request.POST.get("file")
        allowed_extensions = ["pdf", "docs", "docx", "xlsx", "json"]
        file_extension = file.split(".")[-1]
        extension_valid = False if file else True
        if file_extension in allowed_extensions:
            extension_valid = True
        if not (text_data or file):
            context = self.get_context_data(error_message="No data provided")
        elif extension_valid:
            ingest = Ingest.objects.create(text_data=text_data, file=file)
            ingest_data.delay(ingest.id)
            context = self.get_context_data(success_message="File is being processed.")
        else:
            context = self.get_context_data(error_message="Invalid file extension.")

        return self.render_to_response(context)
