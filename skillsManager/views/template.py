from iommi import Column, Form, Page, Table

from skillsManager.models import Template


class TemplateView(Page):
    template_table = Table(
        auto__model=Template,
        page_size=10,
        columns__template__include=False,
        columns__edit=Column.edit(),
        columns__delete=Column.delete(),
    )
    new_template = Form.create(
        title="New template",
        auto__model=Template,
        extra__redirect_to=".",
        fields__template__input__attrs__style__height="40em",
    )


template_edit = Form.edit(
    auto__model=Template,
    instance=lambda pk, **_: Template.objects.get(pk=pk),
    fields__template__input__attrs__style__height="40em",
)

template_delete = Form.delete(instance=lambda pk, **_: Template.objects.get(pk=pk))
