import io
from django import forms
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from weasyprint import HTML
from ..models import Profile
from django.template import loader
from iommi import Page, Form, Field, html


class CVSelectProfileForm(forms.Form):
    profile = forms.ModelChoiceField(queryset=Profile.objects)


def view(request):
    if request.method == "POST":
        form = CVSelectProfileForm(request.POST)
        if form.is_valid():
            template = loader.get_template("cvreport.html")
            pdf = HTML(
                string=template.render({"profile": form.cleaned_data["profile"]})
            )
            buffer = io.BytesIO()
            pdf.write_pdf(buffer)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename="cv.pdf")
    else:
        form = CVSelectProfileForm()
    return HttpResponse(render(request, "cv.html", {"form": form}))


class CVPage(Page):
    def do_export(form, page, **_):
        if form.is_valid():
            template = loader.get_template("cvreport.html")
            pdf = HTML(
                string=template.render({"profile": form.fields["profile"].value})
            )
            buffer = io.BytesIO()
            pdf.write_pdf(buffer)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename="cv.pdf")

    title = html.h1("CV exporter")

    profile_select = Form(
        fields__profile=Field.choice_queryset(Profile.objects, model=Profile),
        actions__submit__post_handler=do_export,
    )
