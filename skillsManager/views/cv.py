import io

from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import Context
from django.template import Template as DjangoTemplate
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.urls import reverse
from iommi import Action, Page, Form, Field, html

from ..models import (
    Profile,
    Template,
    ProfileSkillReference,
    ProfileMeta,
    Language,
    Education,
    ProfileProjectReference,
    ProfileProjectSkillReference,
    ProfileCertificateReference, Skill,
)


def get_context(profile):
    project_works = []
    for project_work in ProfileProjectReference.objects.filter(
            profile=profile
    ).order_by("-active_since"):
        project_works.append(
            dict(
                project_work=project_work,
                skills=ProfileProjectSkillReference.objects.filter(
                    profile_project_reference=project_work
                ),
            )
        )

    raw_categories = []

    skills = []
    for profile_skill in ProfileSkillReference.objects.filter(profile=profile).order_by(
            "-level"
    ):
        skills.append(Skill.objects.get(pk=profile_skill.skill.pk))
        if profile_skill.skill.category is not None and profile_skill.skill.category not in raw_categories:
            raw_categories.append(profile_skill.skill.category)

    context_categories = []

    for raw_category in raw_categories:
        context_category = {
            "name": raw_category.name,
            "description": raw_category.description,
            "skills": [],
        }
        category_skills = raw_category.skill_set.all()
        for skill in skills:
            if skill in category_skills:
                context_category["skills"].append(skill)
        context_categories.append(context_category)

    return Context(
        dict(
            profile=profile,
            profile_meta=ProfileMeta.objects.get(profile=profile),
            languages=Language.objects.filter(profile=profile),
            educations=Education.objects.filter(profile=profile),
            certificates=ProfileCertificateReference.objects.filter(profile=profile),
            project_works=project_works,
            skills=skills,
            skill_categories=context_categories
        )
    )


def do_export(form, **_):
    if form.is_valid():
        template = form.fields["template"].value
        profile = form.fields["profile"].value
        return HttpResponseRedirect(reverse("cv-export", kwargs={"template_pk": template.pk, "profile_pk": profile.pk}))
    return None


def do_preview(form, page, **_):
    if form.is_valid():
        template = DjangoTemplate(form.fields["template"].value.template)
        page.parts["preview"].attrs.srcdoc = template.render(
            context=get_context(form.fields["profile"].value)
        )
    else:
        page.parts["preview"].attrs.srcdoc = ""


def export_func(_, template_pk, profile_pk):
    try:
        template = Template.objects.get(pk=template_pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Template not found")
    try:
        profile = Profile.objects.get(pk=profile_pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Profile not found")
    cv = DjangoTemplate(template.template)
    return HttpResponse(cv.render(
        context=get_context(profile)
    ))


class CVPage(Page):
    title = html.h1(_("CV exporter"))

    profile_select = Form(
        extra__preview="",
        fields__profile=Field.choice_queryset(choices=Profile.objects.all(), display_name=_("Profile"), model=Profile),
        fields__template=Field.choice_queryset(
            choices=Template.objects.all(),
            display_name=_("Template"),
            model=Template,
            initial=lambda **_: (
                Template.objects.first() if Template.objects.count() > 0 else None
            ),
        ),
        actions__preview=Action.button(
            display_name=_("Preview"), attrs__name="-preview", post_handler=do_preview
        ),
        actions__export=Action.primary(display_name=_("Export"), post_handler=do_export),
    )

    preview = html.iframe(attrs__class__preview=True, attrs__srcdoc="")
