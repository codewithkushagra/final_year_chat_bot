from django.urls import path

from apps.ingest.views import IngestDataView


app_name = 'ingest'


urlpatterns = [
    path('data/', IngestDataView.as_view(), name='ingest_data'),
]
