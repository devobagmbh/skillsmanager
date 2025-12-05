from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from iommi import Form, Field, Page, html, EditTable, EditColumn

from skillsManager.middleware.auth import has_permission_lambda
from skillsManager.models import Project, Customer, ProjectLog

project_edit = Form.edit(
    auto__model=Project,
    instance=lambda pk, **_: Project.objects.get(pk=pk),
    fields__customer=Field.non_rendered(initial=lambda customer_pk, **_: Customer.objects.get(pk=customer_pk)),
    editable=has_permission_lambda("skillsManager.change_project"),
    actions__submit__include=has_permission_lambda("skillsManager.change_project"),
)

project_delete = Form.delete(
    instance=lambda pk, **_: Project.objects.get(pk)
)


class ProjectLogView(Page):
    back = html.div(
        children__backlink=html.a(
            _("← Back to customer"),
            attrs__href=lambda customer_pk, **_: reverse(
                "customer-edit",
                kwargs={
                    "pk": customer_pk,
                }
            ),
        )
    )
    back_hr = html.br(attrs__clear="all")
    project_logs = EditTable(
        auto__model=ProjectLog,
        columns__project__field=Field.non_rendered(
            initial=lambda pk, **_: Project.objects.get(pk=pk)
        ),
        columns__delete=EditColumn.delete(include=has_permission_lambda("skillsManager.delete_projectlog")),
        columns__timestamp__field__initial=lambda instance, **_: instance.timestamp if instance else now(),
        edit_actions__add_row__include=has_permission_lambda("skillsManager.add_projectlog"),
        edit_actions__save__include=has_permission_lambda("skillsManager.change_projectlog"),
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        },
    )
