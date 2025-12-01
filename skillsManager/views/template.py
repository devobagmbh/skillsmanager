from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from iommi import Column, Form, Page, Table, html

from skillsManager.models import Template


class TemplateView(Page):
    template_table = Table(
        title=_("Templates"),
        auto__model=Template,
        page_size=10,
        columns__template__include=False,
        columns__edit=Column.edit(),
        columns__delete=Column.delete(),
    )
    new_template = Form.create(
        title=_("New template"),
        auto__model=Template,
        extra__redirect_to=".",
        fields__template__input__attrs__style__height="40em",
    )


class TemplateEdit(Page):
    back = html.div(
        children__backlink=html.a(
            _("← Back to templates"),
            attrs__href=lambda **_: reverse("main_menu.templates"),
        )
    )
    back_hr = html.br(attrs__clear="all")
    template_edit = Form.edit(
        auto__model=Template,
        instance=lambda pk, **_: Template.objects.get(pk=pk),
        fields__template__input__attrs__style__height="40em",
    )


template_delete = Form.delete(instance=lambda pk, **_: Template.objects.get(pk=pk))
