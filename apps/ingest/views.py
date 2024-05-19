from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.utils.utils import SideBarSelectedMixin


class IngestDataView(LoginRequiredMixin, SideBarSelectedMixin, generic.TemplateView):
    template_name = "pages/integrations/data_ingestion/data_ingestion.html"
    parent = "ingest"
    segment = "ingest_data"
