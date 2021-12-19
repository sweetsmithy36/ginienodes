from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages import views as flatpage_views
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views import defaults as default_views
from django.views.generic import TemplateView
from filebrowser.sites import site as filebrowser

from coinginie.core.views import (
    DashboardTradeView,
    DashboardView,
    MyPasswordChangeView,
    MyPasswordSetView,
)
from config.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("dashboard/", DashboardView.as_view(),name='dashboard'),
    path("dashboard/MT5/", DashboardTradeView.as_view(),name='dashboard-trade'),

    # Django Admin, use {% url 'admin:index' %}
    # path('jet/', include('jet.urls', namespace='jet')),
    # path('jet/dashboard/', include('jet.dashboard.urls', namespace='jet-dashboard')),
    path(_("admin/"), include("admin_honeypot.urls", namespace="admin_honeypot")),
    path(_(settings.ADMIN_URL), admin.site.urls),
    path(_(settings.ADMIN_DOC_URL), include("django.contrib.admindocs.urls")),
    path(_(settings.ADMIN_FILEBROWSER_URL), filebrowser.urls),


    # User management
    path("users/", include("coinginie.users.urls", namespace="users")),
    path("wallet/", include("coinginie.wallet.urls", namespace="wallet")),
    path("accounts/", include("allauth.urls")),


    # Your stuff: custom urls includes go here
    path('auth-logout/',TemplateView.as_view(template_name="account/logout-success.html"),name ='pages-logout'),
    path('auth-lockscreen/',TemplateView.as_view(template_name="account/lock-screen.html"),name ='pages_lockscreen'),
    #Custum change password done page redirect
    path('accounts/password/change/', login_required(MyPasswordChangeView.as_view()), name="account_change_password"),
    #Custum set password done page redirect
    path('accounts/password/set/', login_required(MyPasswordSetView.as_view()), name="account_set_password"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# flatpages
if flatpage_views:
    urlpatterns += [
        path(_("terms/"), flatpage_views.flatpage, {"url":"/terms/"}, name="terms"),
        path(_("cookies/"), flatpage_views.flatpage, {"url":"/cookies/"}, name="cookies"),
        path(_("privacy/"), flatpage_views.flatpage, {"url":"/privacy/"}, name="privacy"),
    ]


# Translation urls
urlpatterns += [
    # path('rosetta/', include('rosetta.urls')),
    path('upload/', include('django_file_form.urls')),
    path('tinymce/', include('tinymce.urls')),
    # Language switcher support urls for django
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += [
    path("sitemap.xml/", sitemap, kwargs={"sitemaps": sitemaps}, name="sitemap"),
    path(
        "robots.txt/",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

admin.site.site_header = "Dashboard - Ginie Nodes"
admin.site.site_title = "Ginie Nodes DB"
admin.site.index_title = "Ginie Nodes DB"
