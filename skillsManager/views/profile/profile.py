from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from iommi import (
    EditColumn,
    EditTable,
    Field,
    Form,
    Table,
    Column,
    Page,
    html, )

from skillsManager.middleware.auth import has_permission_lambda
from skillsManager.models import (
    Profile,
    ProfileMeta,
    Language,
    Education,
)
from skillsManager.widgets import range_field


class ProfileEdit(Page):
    back_to_profiles = html.div(
        children__backlink=html.a(
            _("← Back to profiles"),
            attrs__href=lambda **_: reverse("main_menu.profiles"),
        )
    )
    back_to_profiles_br = html.br(attrs__clear="all")
    edit_profile = Form.edit(
        title=_("Profile"),
        auto__model=Profile,
        instance=lambda pk, **_: Profile.objects.get(pk=pk),
        editable=has_permission_lambda("skillsManager.change_profile"),
        actions__submit__include=has_permission_lambda("skillsManager.change_profile"),
    )
    edit_meta = Form.create_or_edit(
        title=_("Personal data"),
        auto__model=ProfileMeta,
        instance=lambda pk, **_: (
            ProfileMeta.objects.get(profile=Profile.objects.get(pk=pk))
            if ProfileMeta.objects.filter(profile=Profile.objects.get(pk=pk)).count()
               == 1
            else None
        ),
        fields__description__input__attrs__rows=10,
        fields__maturity_level=range_field(1, 10, include=True, display_name=_("Maturity level")),
        fields__profile=Field.non_rendered(
            initial=lambda pk, **_: Profile.objects.get(pk=pk)
        ),
        include=has_permission_lambda("skillsManager.view_profilemeta"),
        editable=has_permission_lambda("skillsManager.change_profilemeta"),
        actions__submit__include=has_permission_lambda("skillsManager.change_profilemeta"),
    )
    languages = EditTable(
        title=_("Languages"),
        auto__model=Language,
        rows=lambda pk, **_: Language.objects.filter(profile__pk=pk),
        columns__profile__field=Field.non_rendered(
            initial=lambda pk, **_: Profile.objects.get(pk=pk)
        ),
        include=has_permission_lambda("skillsManager.view_language"),
        columns__language__field__include=has_permission_lambda("skillsManager.change_language"),
        columns__delete=EditColumn.delete(include=has_permission_lambda("skillsManager.delete_language")),
        edit_actions__save__include=has_permission_lambda("skillsManager.change_language"),
        edit_actions__add_row__include=has_permission_lambda("skillsManager.add_language"),
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        },
    )
    education = EditTable(
        title=_("Education"),
        auto__model=Education,
        rows=lambda pk, **_: Education.objects.filter(profile__pk=pk),
        columns__profile__field=Field.non_rendered(
            initial=lambda pk, **_: Profile.objects.get(pk=pk)
        ),
        include=has_permission_lambda("skillsManager.view_education"),
        columns__delete=EditColumn.delete(include=has_permission_lambda("skillsManager.delete_education")),
        edit_actions__save__include=has_permission_lambda("skillsManager.change_education"),
        edit_actions__add_row__include=has_permission_lambda("skillsManager.add_education"),
        columns__name__field__include=has_permission_lambda("skillsManager.change_education"),
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        },
    )


class ProfileView(Page):
    profile_view = Table(
        title=_("Profiles"),
        auto__model=Profile,
        page_size=10,
        columns__birthday=Column(
            display_name=_("Birthday"),
            include=has_permission_lambda("skillsManager.view_profilemeta"),
            cell__value=lambda row, **_: (
                ProfileMeta.objects.get(profile=row).birthday
                if ProfileMeta.objects.filter(profile=row).count() == 1
                else ""
            ),
        ),
        columns__photo=Column(
            display_name=_("Photo"),
            include=has_permission_lambda("skillsManager.view_profilemeta"),
            cell__value=lambda row, **_: (
                ProfileMeta.objects.get(profile=row).photo.url
                if ProfileMeta.objects.filter(profile=row).count() == 1
                   and ProfileMeta.objects.get(profile=row).photo.name != ""
                else ""
            ),
            cell__format=lambda value, **_: (
                mark_safe('<img src="%s" />' % value) if value != "" else ""
            ),
            cell__attrs__style={"max-width": "4em", "max-height": "4em"},
        ),
        columns__skills=Column.link(
            display_name=_("Skills"),
            include=has_permission_lambda("skillsManager.view_profileskillreference"),
            attr=None,
            cell__url=lambda row, **_: reverse_lazy(
                "profileskills-list", kwargs=dict(profile_pk=row.pk)
            ),
            cell__value=_("Skills"),
        ),
        columns__certificates=Column.link(
            display_name=_("Certificates"),
            include=has_permission_lambda("skillsManager.view_profilecertificatereference"),
            attr=None,
            cell__url=lambda row, **_: reverse_lazy(
                "profilecertificates-list", kwargs=dict(profile_pk=row.pk)
            ),
            cell__value=_("Certificates"),
        ),
        columns__projectwork=Column.link(
            display_name=_("Project work"),
            include=has_permission_lambda("skillsManager.view_profileprojectreference"),
            attr=None,
            cell__url=lambda row, **_: reverse_lazy(
                "projectwork-list", kwargs=dict(profile_pk=row.pk)
            ),
            cell__value=_("Project work"),
        ),
        columns__edit=Column.edit(include=has_permission_lambda("skillsManager.view_profile")),
        columns__delete=Column.delete(include=has_permission_lambda("skillsManager.delete_profile")),
    )
    new_profile = Form.create(
        title=_("New profile"),
        auto__model=Profile,
        extra__redirect=lambda form, **_: redirect("profile-edit", pk=form.instance.pk),
        include=has_permission_lambda("skillsManager.add_profile"),
    )


profile_delete = Form.delete(
    instance=lambda pk, **_: Profile.objects.get(pk=pk),
)
