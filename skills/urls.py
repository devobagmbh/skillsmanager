import os
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("skillsManager.urls")),
    path("", RedirectView.as_view(url="/home")),
    (
        path(
            "azure_auth/",
            include("azure_auth.urls"),
        )
        if os.environ.get("AZURE_ENABLED", "false").lower() == "true"
        else path("accounts/", include("django.contrib.auth.urls"))
    ),
]
