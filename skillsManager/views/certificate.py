from iommi import Column, EditColumn, EditTable, Field, Form, Page, Table
from skillsManager.models import Certificate, CertificateVendor
from iommi.form import save_nested_forms


class VendorEdit(Form):
    edit_vendor = Form.edit(
        title="Vendor",
        auto__model=CertificateVendor,
        instance=lambda pk, **_: CertificateVendor.objects.get(pk=pk),
    )
    certificates = EditTable(
        title="Certificates",
        auto__model=Certificate,
        rows=lambda pk, **_: Certificate.objects.filter(vendor__pk=pk),
        columns__vendor__field=Field.non_rendered(
            initial=lambda pk, **_: CertificateVendor.objects.get(pk=pk)
        ),
        columns__delete=EditColumn.delete(),
        columns__name__field__include=True,
        columns__description__field__include=True,
        **{
            "attrs__data-iommi-edit-table-delete-with": "checkbox",
        }
    )

    class Meta:
        actions__submit__post_handler = save_nested_forms
        extra__redirect_to = lambda **_: "/certificates"


class VendorView(Page):
    vendors = Table(
        auto__model=CertificateVendor,
        page_size=10,
        columns__certificates=Column(
            cell__value=lambda row, **_: Certificate.objects.filter(vendor=row)
        ),
        columns__edit=Column.edit(),
        columns__delete=Column.delete(),
    )
    new_vendor = Form.create(
        title="New certificate vendor",
        auto__model=CertificateVendor,
        extra__redirect_to=".",
    )


vendor_delete = Form.delete(
    instance=lambda pk, **_: CertificateVendor.objects.get(pk=pk)
)
