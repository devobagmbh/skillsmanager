from django.shortcuts import redirect
from django.template import Template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from iommi import Page, Form, Table, Column, Field, html, Panel

from skillsManager.models import ProfileSkillReference, Profile, Skill
from skillsManager.widgets import range_field


class ProfileSkillEdit(Page):
    skill = Form.edit(
        title=_("Edit skill"),
        auto__model=ProfileSkillReference,
        instance=lambda pk, **_: ProfileSkillReference.objects.get(pk=pk),
        fields__level=range_field(1, 10, include=True),
        fields__favorite=range_field(1, 10, include=True),
        extra__redirect=lambda profile_pk, **_: redirect(
            reverse("profileskills-list", kwargs={"profile_pk": profile_pk})),
    )


class ProfileSkillView(Page):
    back_to_profiles = html.div(
        children__backlink=html.a(
            _("← Back to profiles"),
            attrs__href=lambda **_: reverse("main_menu.profiles"),
        )
    )
    back_to_profiles_br = html.br(attrs__clear="all")
    skills = Table(
        auto__model=ProfileSkillReference,
        page_size=10,
        rows=lambda profile_pk, **_: ProfileSkillReference.objects.filter(profile_id=profile_pk),
        columns__edit=Column.edit(),
        columns__delete=Column.delete(),
    )

    new_skill_modal = html.div(
        attrs__class__reveal=True, **{"attrs__data-reveal": True},
        attrs__id="new-skill-modal",
        children__close=html.button(
            attrs__type="button",
            children__content=html.span("×", **{"attrs__aria-hidden": "true"}),
            **{"attrs__data-close": True, "attrs__aria-label": "Close", "attrs__class__close-button": True},
        ),
        children__new_skill=Form.create(
            title="New skill",
            auto__model=Skill,
            extra__redirect_to=".",

        ),
    )

    new_skill_reference = Form.create(
        title=_("New skill reference"),
        auto__model=ProfileSkillReference,
        fields__new_skill=Field(
            attr=None,
            required=False,
            group="skill",
            template=Template(
                mark_safe(
                    '<button type="button" class="button" data-open="new-skill-modal" aria-controls="new-skill-modal" aria-haspopup="true" tabindex="0">+</button>'
                )
            )
        ),
        fields__level=range_field(1, 10, include=True),
        fields__favorite=range_field(1, 10, include=True),
        extra__redirect_to=".",
        fields__profile=Field.non_rendered(
            initial=lambda profile_pk, **_: Profile.objects.get(pk=profile_pk)
        ),
        layout=Panel(dict(
            p_main=Panel.div(dict(
                p_skills=Panel.fieldset(dict(
                    skill=Panel.field(),
                    new_skill=Panel.field(),
                )),
                level=Panel.field(),
                favorite=Panel.field(),
                remarks=Panel.field(),
            )),
        ))
    )


profile_skill_delete = Form.delete(
    instance=lambda profile_pk, pk, **_: ProfileSkillReference.objects.get(profile_id=profile_pk, pk=pk)
)
