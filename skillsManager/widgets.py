from iommi import Field, html
from django.utils.safestring import mark_safe


def range_field(min, max, **kwargs):
    return Field(
        input__attrs__type="range",
        input__attrs__min=min,
        input__attrs__max=max,
        input__template="widgets/range.html",
        **kwargs
    )


def range_field_helper():
    return html.script(
        mark_safe(
            """
            document.addEventListener("iommi.editTable.newElement", (event) => {
                jQuery("input[type=range] ~ script", event.target).each((_, element) => {eval(element.textContent)}) 
            });
            """
        )
    )
