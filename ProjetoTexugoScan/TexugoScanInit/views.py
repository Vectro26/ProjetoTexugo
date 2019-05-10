from django.views.generic.base import TemplateView


class IndexTemplateView(TemplateView):
    template_name = "Templates/index.html"
