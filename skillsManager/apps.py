from django.apps import AppConfig
from django.template.loader import get_template
from iommi import register_style, Style, Asset, style_foundation


def azure_user_mapping_fn(**attributes):
    return {
        "full_name": attributes["givenName"] + attributes["surname"],
        "email": attributes["mail"],
        "is_staff": True,
    }


class SkillsmanagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "skillsManager"

    def ready(self):
        register_style(
            "skills",
            Style(
                style_foundation.foundation,
                root__assets__skills_css=Asset(
                    tag="style",
                    text=get_template(template_name="style.css").render(dict()),
                ),
                root__assets__easymde_css=Asset.css(
                    attrs__href="https://unpkg.com/easymde/dist/easymde.min.css"
                ),
                root__assets__easymds_js=Asset.js(
                    attrs__src="https://unpkg.com/easymde/dist/easymde.min.js"
                ),
                root__assets__favicon=Asset(template="favicon.html"),
                root__assets__foundation_call=Asset(template="foundationcall.html", in_body=True)
            ),
        )
