from iommi import Page, html


class HomePage(Page):
    header = html.header(
        children=dict(
            title=html.h1("skills Manager"),
            subtitle=html.p(
                "Management of skills, certificates and projects for consulting companies."
            ),
        )
    )
    body_text = "Welcome to skills Manager. Please select a menu option on the left."
