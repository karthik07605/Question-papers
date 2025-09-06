from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .views import home
from .sitemaps import StaticViewSitemap, PaperSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "papers": PaperSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),  # added name for sitemap
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
