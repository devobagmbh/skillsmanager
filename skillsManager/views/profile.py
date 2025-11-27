from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from iommi import (
    EditColumn,
    EditTable,
    Field,
    Form,
    Table,
    Column,
    Page,
    html, Action,
)
from iommi.form import save_nested_forms

from ..models import (
    Profile,
    ProfileMeta,
    ProfileSkillReference,
    ProfileCertificateReference,
    Language,
    Education,
)
from ..widgets import range_field, range_field_helper


class ProfileEdit(Form):
    edit_profile = Form.edit(
        title="Profile",
        auto__model=Profile,
        instance=lambda pk, **_: Profile.objects.get(pk=pk),
    )
    edit_meta = Form.create_or_edit(
        title="Personal data",
        auto__model=ProfileMeta,
        instance=lambda pk, **_: (
            ProfileMeta.objects.get(profile=Profile.objects.get(pk=pk))
            if ProfileMeta.objects.filter(profile=Profile.objects.get(pk=pk)).count()
               == 1
            else None
        ),
        fields__description__input__attrs__rows=10,
        fields__maturity_level=range_field(1, 10, include=True),
        fields__profile=Field.non_rendered(
            initial=lambda pk, **_: Profile.objects.get(pk=pk)
        ),
    )
    languages = EditTable(
        title="Languages",
        auto__model=Language,
        rows=lambda pk, **_: Language.objects.filter(profile__pk=pk),
        columns__profile__field=Field.non_rendered(
            initial=lambda pk, **_: Profile.objects.get(pk=pk)
        ),
        columns__language__field__include=True,
        columns__delete=EditColumn.delete(),
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        },
    )
    education = EditTable(
        title="Education",
        auto__model=Education,
        rows=lambda pk, **_: Education.objects.filter(profile__pk=pk),
        columns__profile__field=Field.non_rendered(
            initial=lambda pk, **_: Profile.objects.get(pk=pk)
        ),
        columns__name__field__include=True,
        columns__delete=EditColumn.delete(),
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        },
    )
    skills_hr = html.hr()
    skills = EditTable(
        title="Skills",
        auto__model=ProfileSkillReference,
        rows=lambda pk, **_: ProfileSkillReference.objects.filter(profile__pk=pk),
        columns__profile__field=Field.non_rendered(
            initial=lambda pk, **_: Profile.objects.get(pk=pk)
        ),
        columns__level__field=range_field(1, 10, include=True),
        columns__favorite__field=range_field(1, 10, include=True),
        columns__remarks__field__include=True,
        columns__delete=EditColumn.delete(),
        outer__children__rangehelper=range_field_helper(),
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        },
    )

    class Meta:
        actions__submit__post_handler = save_nested_forms
        extra__redirect_to = lambda **_: "/profiles"


class ProfileView(Page):
    profile_view = Table(
        auto__model=Profile,
        page_size=10,
        columns__birthday=Column(
            cell__value=lambda row, **_: (
                ProfileMeta.objects.get(profile=row).birthday
                if ProfileMeta.objects.filter(profile=row).count() == 1
                else ""
            ),
        ),
        columns__photo=Column(
            cell__value=lambda row, **_: (
                ProfileMeta.objects.get(profile=row).photo.url
                if ProfileMeta.objects.filter(profile=row).count() == 1
                   and ProfileMeta.objects.get(profile=row).photo.name != ""
                else ""
            ),
            cell__format=lambda value, **_: (
                mark_safe('<img src="%s" />' % (value)) if value != "" else ""
            ),
            cell__attrs__style={"max-width": "4em", "max-height": "4em"},
        ),
        columns__certificates=Column.link(
            attr=None,
            cell__url=lambda row, **_: reverse_lazy(
                "profilecertificates-list", kwargs=dict(profile_pk=row.pk)
            ),
            cell__value="Certificates",
        ),
        columns__projectwork=Column.link(
            attr=None,
            cell__url=lambda row, **_: reverse_lazy(
                "projectwork-list", kwargs=dict(profile_pk=row.pk)
            ),
            cell__value="Project work",
        ),
        columns__edit=Column.edit(),
        columns__delete=Column.delete(),
    )
    new_profile = Form.create(
        title="New profile",
        auto__model=Profile,
        extra__redirect=lambda form, **_: redirect("profile-edit", pk=form.instance.pk),
    )


profile_delete = Form.delete(
    instance=lambda pk, **_: Profile.objects.get(pk=pk),
)


def delete_certificate_file(instance, **kwargs):
    instance.file = None
    instance.save()
    return HttpResponseRedirect(instance.get_absolute_url())


def download_certificate(instance, **kwargs):
    return HttpResponseRedirect(instance.file.url)


class ProfileCertificateEdit(Page):
    certificate = Form.edit(
        title="Edit certificate",
        auto__model=ProfileCertificateReference,
        instance=lambda pk, **_: ProfileCertificateReference.objects.get(pk=pk),
        actions__download=Action.submit(
            display_name="Download certificate",
            post_handler=download_certificate,
            include=lambda pk, **_: ProfileCertificateReference.objects.get(pk=pk).file,
        ),
        actions__clear=Action.submit(
            display_name="Delete certificate file",
            post_handler=delete_certificate_file,
            include=lambda pk, **_: ProfileCertificateReference.objects.get(pk=pk).file,
        ),
        extra__redirect=lambda profile_pk, **_: redirect(
            reverse("profilecertificates-list", kwargs={"profile_pk": profile_pk})),
    )


class ProfileCertificateView(Page):
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
