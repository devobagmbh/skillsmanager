from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from iommi import Column, EditColumn, EditTable, Field, Form, Page, Table, html
from iommi.form import save_nested_forms

from skillsManager.models import Project, ProjectLog, Customer, CustomerLog


class CustomerEdit(Form):
    back = html.div(
        children__backlink=html.a(
            _("← Back to customers"),
            attrs__href=lambda **_: reverse("main_menu.projects"),
        )
    )
    back_hr = html.br(attrs__clear="all")
    edit_customer = Form.edit(
        title=_("Customer"),
        auto__model=Customer,
        instance=lambda pk, **_: Customer.objects.get(pk=pk),
    )
    projects = EditTable(
        title=_("Projects"),
        auto__model=Project,
        rows=lambda pk, **_: Project.objects.filter(customer__pk=pk),
        columns__customer__field=Field.non_rendered(
            initial=lambda pk, **_: Customer.objects.get(pk=pk)
        ),
        columns__delete=EditColumn.delete(),
        columns__name__field__include=True,
        columns__description__field__include=True,
        columns__active_since__field__include=True,
        columns__active_since__field__initial=lambda instance, **_: instance.active_since if instance else now(),
        columns__active_until__field__include=True,
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        }
    )
    logs = EditTable(
        title=_("Customer logs"),
        auto__model=CustomerLog,
        rows=lambda pk, **_: CustomerLog.objects.filter(customer__pk=pk),
        columns__delete=EditColumn.delete(),
        columns__notice__field__include=True,
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        }
    )
    project_logs = EditTable(
        title=_("Project logs"),
        auto__model=ProjectLog,
        page_size=10,
        rows=lambda pk, **_: ProjectLog.objects.filter(project__customer__pk=pk),
        columns__timestamp__field__initial=lambda instance, **_: instance.timestamp if instance else now(),
        columns__notice__field__include=True,
        # columns__project__filter__include=True,
    )

    class Meta:
        actions__submit__post_handler = save_nested_forms
        extra__redirect_to = lambda **_: "/projects"


class CustomerView(Page):
    customers = Table(
        title=_("Customers"),
        auto__model=Customer,
        page_size=10,
        columns__projects=Column(
            cell__value=lambda row, **_: Project.objects.filter(customer=row)
        ),
        columns__edit=Column.edit(),
        columns__delete=Column.delete(),
    )
    new_customer = Form.create(
        title=_("New customer"),
        auto__model=Customer,
        extra__redirect_to=".",
    )


customer_delete = Form.delete(instance=lambda pk, **_: Customer.objects.get(pk=pk))
