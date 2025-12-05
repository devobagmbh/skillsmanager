from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from iommi import Column, EditColumn, Form, Page, Table, html, Field, EditTable

from skillsManager.middleware.auth import has_permission_lambda
from skillsManager.models import Project, Customer, CustomerLog


class CustomerEdit(Page):
    back = html.div(
        children__backlink=html.a(
            _("← Back to customers"),
            attrs__href=lambda **_: reverse("main_menu.customers"),
        )
    )
    back_hr = html.br(attrs__clear="all")
    customer = Form.edit(
        title=_("Customer"),
        auto__model=Customer,
        instance=lambda pk, **_: Customer.objects.get(pk=pk),
        editable=has_permission_lambda("skillsManager.change_customer"),
        actions__submit__include=has_permission_lambda("skillsManager.change_customer"),
    )
    projects = Table(
        title=_("Projects"),
        auto__model=Project,
        rows=lambda pk, **_: Project.objects.filter(customer__pk=pk),
        columns__log=Column.link(
            display_name=_("Project log"),
            attr=None,
            cell__url=lambda pk, row, **_: reverse_lazy(
                "projects-log", kwargs=dict(customer_pk=pk, pk=row.pk)
            ),
            cell__value=_("Project log"),
        ),
        columns__edit=EditColumn.edit(
            include=has_permission_lambda("skillsManager.view_project")
        ),
        columns__delete=EditColumn.delete(include=has_permission_lambda("skillsManager.delete_project")),
    )
    new_project = Form.create(
        title=_("New project"),
        auto__model=Project,
        fields__customer=Field.non_rendered(initial=lambda pk, **_: Customer.objects.get(pk=pk)),
        include=has_permission_lambda("skillsManager.add_project"),
    )


class CustomerView(Page):
    customers = Table(
        title=_("Customers"),
        auto__model=Customer,
        page_size=10,
        columns__projects=Column(
            cell__value=lambda row, **_: Project.objects.filter(customer=row)
        ),
        columns__log=Column.link(
            display_name=_("Customer log"),
            attr=None,
            cell__url=lambda row, **_: reverse_lazy(
                "customer-logs", kwargs=dict(pk=row.pk)
            ),
            cell__value=_("Customer log"),
            include=has_permission_lambda("skillsManager.view_projectlog")
        ),
        columns__edit=Column.edit(include=has_permission_lambda("skillsManager.view_customer")),
        columns__delete=Column.delete(include=has_permission_lambda("skillsManager.delete_customer")),
    )
    new_customer = Form.create(
        title=_("New customer"),
        auto__model=Customer,
        extra__redirect_to=".",
        include=has_permission_lambda("skillsManager.add_customer"),
    )


customer_delete = Form.delete(instance=lambda pk, **_: Customer.objects.get(pk=pk))


class CustomerLogView(Page):
    back = html.div(
        children__backlink=html.a(
            _("← Back to customers"),
            attrs__href=lambda **_: reverse("main_menu.customers"),
        )
    )
    back_hr = html.br(attrs__clear="all")
    customer_log = EditTable(
        auto__model=CustomerLog,
        columns__customer__field=Field.non_rendered(
            initial=lambda pk, **_: Customer.objects.get(pk=pk)
        ),
        columns__timestamp__field__initial=lambda instance, **_: instance.timestamp if instance else now(),
        columns__delete=EditColumn.delete(include=has_permission_lambda("skillsManager.delete_projectlog")),
        edit_actions__add_row__include=has_permission_lambda("skillsManager.add_projectlog"),
        edit_actions__save__include=has_permission_lambda("skillsManager.change_projectlog"),
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        },
    )
