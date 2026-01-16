from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from iommi import Column, Field, Form, Page, Table, html

from skillsManager.middleware.auth import has_permission_lambda
from skillsManager.models import (
    Profile,
    ProfileProjectReference,
    ProfileSkillReference,
    ProfileProjectSkillReference,
)


class ProjectWorkView(Page):
    back_to_profiles = html.div(
        children__backlink=html.a(
            _("← Back to profiles"),
            attrs__href=lambda **_: reverse("main_menu.profiles"),
        )
    )
    back_to_profiles_br = html.br(attrs__clear="all")
    project_work_table = Table(
        title=_("Project work entries"),
        auto__model=ProfileProjectReference,
        page_size=10,
        rows=lambda profile_pk, **_: ProfileProjectReference.objects.filter(
            profile__pk=profile_pk
        ),
        columns__skills=Column(
            display_name=_("Skills"),
            cell__value=lambda row, **_: ProfileProjectSkillReference.objects.filter(
                profile_project_reference__pk=row.pk
            )
        ),
        columns__remarks__include=False,
        columns__edit=Column.edit(include=has_permission_lambda("skillsManager.view_profileprojectreference")),
        columns__delete=Column.delete(include=has_permission_lambda("skillsManager.delete_profileprojectreference")),
    )
    new_project_work = Form.create(
        title=_("New project work entry"),
        auto__model=ProfileProjectReference,
        extra__redirect_to=".",
        fields__profile=Field.non_rendered(
            initial=lambda profile_pk, **_: Profile.objects.get(pk=profile_pk)
        ),
        fields__remarkseditor=Field.hidden(
            attr=None,
            label__children__script=
            html.script(
                mark_safe(
                    """
                    const easyMDE = new EasyMDE({
                        element: document.getElementById('id_new_project_work__remarks'),
                        hideIcons: "preview",
                    });
                    """
                )
            )
        ),
        fields__remarks__input__attrs__rows="20",
        include=has_permission_lambda("skillsManager.add_profileprojectreference")
    )


def store_skills(form, instance, **_):
    if form.is_valid():
        ProfileProjectSkillReference.objects.filter(
            profile_project_reference=instance.pk
        ).delete()
        for skill_ref in form.fields["skills"].value:
            ref = ProfileProjectSkillReference()
            ref.profile_project_reference = instance
            ref.skill = skill_ref.skill
            ref.save()


def get_initial(profile_pk, pk, **_):
    initial = []
    for profile_project_skill_ref in ProfileProjectSkillReference.objects.filter(
            profile_project_reference=pk
    ):
        profile_skill_refs = ProfileSkillReference.objects.filter(
            skill=profile_project_skill_ref.skill, profile__pk=profile_pk
        )
        if profile_skill_refs.count() == 1:
            initial.append(profile_skill_refs.first())
    return initial


class ProjectWorkEdit(Page):
    back_to_profiles = html.div(
        children__backlink=html.a(
            _("← Back to project work entries"),
            attrs__href=lambda profile_pk, **_: reverse("projectwork-list", kwargs={"profile_pk": profile_pk}),
        )
    )
    back_to_profiles_br = html.br(attrs__clear="all")
    project_work = Form.edit(
        title=_("Project Work entry"),
        auto__model=ProfileProjectReference,
        instance=lambda profile_pk, pk, **_: ProfileProjectReference.objects.get(
            profile_id=profile_pk, pk=pk
        ),
        fields__remarkseditor=Field.hidden(
            attr=None,
            label__children__script=
            html.script(
                mark_safe(
                    """
                    const easyMDE = new EasyMDE({
                        element: document.getElementById('id_remarks'),
                        hideIcons: "preview",
                    });
                    """
                )
            )
        ),
        fields__skills=Field.multi_choice(
            attr=None,
            choices=lambda user, profile_pk, **_: ProfileSkillReference.objects.filter(
                profile__pk=profile_pk
            ).all(),
            initial=get_initial,
            include=has_permission_lambda("skillsManager.change_profileprojectreference")
        ),
        fields__skills_viewonly=Field.text(
            display_name=_("Skills"),
            required=False,
            initial=get_initial,
            include=lambda user, **_: settings.SKILLSMANAGER_USE_RBAC and not user.has_perm(
                "skillsManager.change_profileprojectreference"),
        ),
        editable=has_permission_lambda("skillsManager.change_profileprojectreference"),
        fields__remarks__input__attrs__rows="20",
        extra__on_save=store_skills,
    )


project_work_delete = Form.delete(
    instance=lambda pk, **_: ProfileProjectReference.objects.get(pk=pk)
)
