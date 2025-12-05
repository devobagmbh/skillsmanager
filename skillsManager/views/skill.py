from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from iommi import Column, Form, Page, Table, html

from skillsManager.middleware.auth import has_permission_lambda
from skillsManager.models import Skill


class SkillView(Page):
    skills_table = Table(
        auto__model=Skill,
        page_size=10,
        columns__name__filter__include=True,
        columns__description__filter__include=True,
        columns__edit=Column.edit(include=has_permission_lambda("skillsManager.view_skill")),
        columns__delete=Column.delete(include=has_permission_lambda("skillsManager.delete_skill")),
    )
    new_skill = Form.create(
        title=_("New skill"),
        auto__model=Skill,
        extra__redirect_to=".",
        include=has_permission_lambda("skillsManager.add_skill"),
    )


class SkillEdit(Page):
    back = html.div(
        children__backlink=html.a(
            _("← Back to skills"),
            attrs__href=lambda **_: reverse("main_menu.skills"),
        )
    )
    back_hr = html.br(attrs__clear="all")

    skill_edit = Form.edit(
        auto__model=Skill, instance=lambda pk, **_: Skill.objects.get(pk=pk),
        editable=has_permission_lambda("skillsManager.change_skill"),
        actions__submit__include=has_permission_lambda("skillsManager.change_skill"),
    )


skill_delete = Form.delete(instance=lambda pk, **_: Skill.objects.get(pk=pk))
