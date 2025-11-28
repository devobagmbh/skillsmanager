from django.urls import reverse
from iommi import Column, Field, Form, Page, Table, html

from skillsManager.models import (
    Profile,
    ProfileProjectReference,
    ProfileSkillReference,
    ProfileProjectSkillReference,
)


class ProjectWorkView(Page):
    back_to_profiles = html.div(
        children__backlink=html.a(
            "← Back to profiles",
            attrs__href=lambda **_: reverse("main_menu.profiles"),
        )
    )
    back_to_profiles_br = html.br(attrs__clear="all")
    project_work_table = Table(
        auto__model=ProfileProjectReference,
        page_size=10,
        rows=lambda profile_pk, **_: ProfileProjectReference.objects.filter(
            profile__pk=profile_pk
        ),
        columns__remarks__include=False,
        columns__edit=Column.edit(),
        columns__delete=Column.delete(),
    )
    new_project_work = Form.create(
        title="New project work entry",
        auto__model=ProfileProjectReference,
        extra__redirect_to=".",
        fields__profile=Field.non_rendered(
            initial=lambda profile_pk, **_: Profile.objects.get(pk=profile_pk)
        ),
        fields__remarks__input__attrs__rows="20",
    )


class ProjectWorkEdit(Page):
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

    project_work = Form.edit(
        title="Project Work entry",
        auto__model=ProfileProjectReference,
        instance=lambda profile_pk, pk, **_: ProfileProjectReference.objects.get(
            profile_id=profile_pk, pk=pk
        ),
        fields__skills=Field.multi_choice(
            attr=None,
            choices=lambda profile_pk, **_: ProfileSkillReference.objects.filter(
                profile__pk=profile_pk
            ).all(),
            initial=get_initial,
        ),
        fields__remarks__input__attrs__rows="20",
        extra__on_save=store_skills,
    )


project_work_delete = Form.delete(
    instance=lambda pk, **_: ProfileProjectReference.objects.get(pk=pk)
)
