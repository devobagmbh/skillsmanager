from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from iommi import Page, Form, Action, Table, Column, Field, html

from skillsManager.models import ProfileCertificateReference, Profile


def delete_certificate_file(instance, **_):
    instance.file = None
    instance.save()
    return HttpResponseRedirect(instance.get_absolute_url())


def download_certificate(instance, **_):
    return HttpResponseRedirect(instance.file.url)


class ProfileCertificateEdit(Page):
    certificate = Form.edit(
        title=_("Edit certificate"),
        auto__model=ProfileCertificateReference,
        instance=lambda pk, **_: ProfileCertificateReference.objects.get(pk=pk),
        actions__download=Action.submit(
            display_name=_("Download certificate"),
            post_handler=download_certificate,
            include=lambda pk, **_: ProfileCertificateReference.objects.get(pk=pk).file,
        ),
        actions__clear=Action.submit(
            display_name=_("Delete certificate file"),
            post_handler=delete_certificate_file,
            include=lambda pk, **_: ProfileCertificateReference.objects.get(pk=pk).file,
        ),
        extra__redirect=lambda profile_pk, **_: redirect(
            reverse("profilecertificates-list", kwargs={"profile_pk": profile_pk})),
    )


class ProfileCertificateView(Page):
    back_to_profiles = html.div(
        children__backlink=html.a(
            "← Back to profiles",
            attrs__href=lambda **_: reverse("main_menu.profiles"),
        )
    )
    back_to_profiles_br = html.br(attrs__clear="all")
    certificates = Table(
        auto__model=ProfileCertificateReference,
        page_size=10,
        rows=lambda profile_pk, **_: ProfileCertificateReference.objects.filter(profile_id=profile_pk),
        columns__file=Column(
            cell__value=lambda row, **_: row.file.url if row.file else "",
            cell__format=lambda value, **_: (
                mark_safe('<a href="%s">Download</a>' % value) if value != "" else ""
            ),
        ),
        columns__edit=Column.edit(),
        columns__delete=Column.delete(),
    )

    new_certificate = Form.create(
        title="New certificate",
        auto__model=ProfileCertificateReference,
        extra__redirect_to=".",
        fields__profile=Field.non_rendered(
            initial=lambda profile_pk, **_: Profile.objects.get(pk=profile_pk)
        ),
    )


profile_certificate_delete = Form.delete(
    instance=lambda profile_pk, pk, **_: ProfileCertificateReference.objects.get(profile_id=profile_pk, pk=pk)
)
