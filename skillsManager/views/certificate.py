from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from iommi import Column, EditColumn, EditTable, Field, Form, Page, Table, html

from skillsManager.middleware.auth import has_permission_lambda
from skillsManager.models import Certificate, CertificateVendor


class VendorEdit(Page):
    back = html.div(
        children__backlink=html.a(
            _("← Back to vendors"),
            attrs__href=lambda **_: reverse("main_menu.certificates"),
        )
    )
    back_hr = html.br(attrs__clear="all")
    edit_vendor = Form.edit(
        # Translators: This is the title of certificate vendors
        title=_("Vendor"),
        auto__model=CertificateVendor,
        instance=lambda pk, **_: CertificateVendor.objects.get(pk=pk),
        editable=has_permission_lambda("skillsManager.change_certificatevendor"),
        actions__submit__include=has_permission_lambda("skillsManager.change_certificatevendor")
    )
    certificates = EditTable(
        title=_("Certificates"),
        auto__model=Certificate,
        rows=lambda pk, **_: Certificate.objects.filter(vendor__pk=pk),
        columns__vendor__field=Field.non_rendered(
            initial=lambda pk, **_: CertificateVendor.objects.get(pk=pk)
        ),
        columns__delete=EditColumn.delete(include=has_permission_lambda("skillsManager.delete_certificate")),
        edit_actions__save__include=has_permission_lambda("skillsManager.change_certificate"),
        edit_actions__add_row__include=has_permission_lambda("skillsManager.add_certificate"),
        columns__name__field__include=has_permission_lambda("skillsManager.change_certificate"),
        columns__description__field__include=has_permission_lambda("skillsManager.change_certificate"),
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        }
    )


class VendorView(Page):
    vendors = Table(
        title=_("Vendors"),
        auto__model=CertificateVendor,
        page_size=10,
        columns__certificates=Column(
            display_name=_("Certificates"),
            cell__value=lambda row, **_: Certificate.objects.filter(vendor=row)
        ),
        columns__edit=Column.edit(include=has_permission_lambda("skillsManager.view_certificatevendor")),
        columns__delete=Column.delete(include=has_permission_lambda("skillsManager.delete_certificatevendor")),
    )
    new_vendor = Form.create(
        title=_("New certificate vendor"),
        auto__model=CertificateVendor,
        extra__redirect_to=".",
        include=has_permission_lambda("skillsManager.add_certificatevendor")
    )


vendor_delete = Form.delete(
    instance=lambda pk, **_: CertificateVendor.objects.get(pk=pk)
)
