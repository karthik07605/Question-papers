from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Paper

# Sitemap for static pages
class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return ['home']  # use your url name for homepage

    def location(self, item):
        return reverse(item)


# Sitemap for Papers
class PaperSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Paper.objects.all()

    def lastmod(self, obj):
        return None  # if you had updated_at, put it here
