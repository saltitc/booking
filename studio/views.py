from common.views import TitleMixin
from django.views.generic.base import TemplateView


class HomeTemplateView(TitleMixin, TemplateView):
    """
    Template view, which displays the home page.
    For administration and staff, the number of new applications,
    the admin panel and application management are additionally shown
    """
    template_name = 'studio/index.html'
    title = 'Главная страница'
