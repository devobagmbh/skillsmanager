import os
from django.contrib import admin
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import path, include
from django.views.generic import RedirectView
from iommi.views import auth_views


def media(request, file_path=None):
    from django.conf import settings as cfg

    media_root = getattr(cfg, "MEDIA_ROOT", None)

    if not media_root:
        return HttpResponseBadRequest("Invalid Media Root Configuration")
    if not file_path:
        return HttpResponseBadRequest("Invalid File Path")

    with open(os.path.join(media_root, file_path), "rb") as doc:
        response = HttpResponse(doc.read(), content_type="application/doc")
        response["Content-Disposition"] = "filename=%s" % (file_path.split("/")[-1])
        return response


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("skillsManager.urls")),
    path("", RedirectView.as_view(url="/home")),
    path("media/<str:file_path>", media, name="media"),
]

if os.environ.get("AZURE_ENABLED", "false").lower() == "true":
    urlpatterns.append(path("", include("azure_auth.urls")))
else:
    urlpatterns.append(path("", auth_views()))
