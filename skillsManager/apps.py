from django.apps import AppConfig
from django.template.loader import get_template
from iommi import register_style, Style, Asset, style_foundation


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
                root__assets__favicon=Asset(template="favicon.html"),
            ),
        )
