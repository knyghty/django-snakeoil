from django.views import generic

from .models import Article


class ArticleDetailView(generic.DetailView):
    model = Article

    def get_template_names(self):
        if self.request.GET.get("template_without_obj"):
            return "tests/article_detail_without_obj.html"
        return super().get_template_names()


class TestView(generic.TemplateView):
    template_name = "base.html"


class Jinja2TestView(generic.TemplateView):
    template_name = "base.jinja2"
