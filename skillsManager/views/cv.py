import io
from django import forms
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from weasyprint import HTML
from ..models import (
    Profile,
    Template,
    ProfileSkillReference,
    ProfileMeta,
    Language,
    Education,
    ProfileProjectReference,
    ProfileProjectSkillReference,
    ProfileCertificateReference,
)
from django.template import Template as DjangoTemplate
from django.template import Context
from iommi import Action, Page, Form, Field, html
from iommi.views import HttpResponseRedirect


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

    return Context(
        dict(
            profile=profile,
            profile_meta=ProfileMeta.objects.get(profile=profile),
            languages=Language.objects.filter(profile=profile),
            educations=Education.objects.filter(profile=profile),
            certificates=ProfileCertificateReference.objects.filter(profile=profile),
            project_works=project_works,
            skills=ProfileSkillReference.objects.filter(profile=profile).order_by(
                "-level"
            ),
        )
    )


class CVPage(Page):

    def do_export(form, **_):
        if form.is_valid():
            template = DjangoTemplate(form.fields["template"].value.template)
            pdf = HTML(
                string=template.render(
                    context=get_context(form.fields["profile"].value)
                )
            )
            buffer = io.BytesIO()
            pdf.write_pdf(buffer)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename="cv.pdf")

    def do_preview(form, **_):
        if form.is_valid():
            template = DjangoTemplate(form.fields["template"].value.template)
            form.extra["preview"] = template.render(
                context=get_context(form.fields["profile"].value)
            )
        else:
            form.extra["preview"] = ""
        return HttpResponseRedirect(".")

    title = html.h1("CV exporter")

    profile_select = Form(
        extra__preview="",
        fields__profile=Field.choice_queryset(Profile.objects, model=Profile),
        fields__template=Field.choice_queryset(
            Template.objects,
            model=Template,
            initial=lambda **_: (
                Template.objects.first() if Template.objects.count() > 0 else None
            ),
        ),
        actions__preview=Action.button(
            display_name="Preview", attrs__name="-preview", post_handler=do_preview
        ),
        actions__export=Action.primary(display_name="Export", post_handler=do_export),
        fields__preview=Field(
            tag="iframe",
            attrs__class__preview=True,
            attrs__srcdoc=lambda form, **_: form.extra["preview"],
            required=False,
            after=99,
        ),
    )
