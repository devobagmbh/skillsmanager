from django.urls import reverse
from iommi import Column, Form, Page, Table, html

from skillsManager.models import Skill


class SkillView(Page):
    skills_table = Table(
        auto__model=Skill,
        page_size=10,
        columns__name__filter__include=True,
        columns__description__filter__include=True,
        columns__edit=Column.edit(),
        columns__delete=Column.delete(),
    )
    new_skill = Form.create(
        title="New skill",
        auto__model=Skill,
        extra__redirect_to=".",
    )


class SkillEdit(Page):
    back = html.div(
        children__backlink=html.a(
            "← Back to skills",
            attrs__href=lambda **_: reverse("main_menu.skills"),
        )
    )
    back_hr = html.br(attrs__clear="all")

    skill_edit = Form.edit(
        auto__model=Skill, instance=lambda pk, **_: Skill.objects.get(pk=pk)
    )


skill_delete = Form.delete(instance=lambda pk, **_: Skill.objects.get(pk=pk))
