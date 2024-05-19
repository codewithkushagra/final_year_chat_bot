from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.utils.utils import SideBarSelectedMixin


class DashboardTemplateView(
    LoginRequiredMixin, SideBarSelectedMixin, generic.TemplateView
):
    template_name = "pages/index.html"
    parent = "dashboard"
    segment = "index"
