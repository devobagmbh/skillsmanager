from django.utils.translation import gettext_lazy as _
from iommi import Page, html


class HomePage(Page):
    header = html.header(
        children=dict(
            # Translators: This is the skills manager title
            title=html.h1(_("skills Manager")),
            subtitle=html.p(
                # Translators: This is the skills manager subtitle
                _("Management of skills, certificates and projects for consulting companies.")
            ),
        )
    )
    body_text = _("Welcome to skills Manager. Please select a menu option on the left.")
