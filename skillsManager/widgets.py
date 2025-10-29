from iommi import Field


def range_field(min, max, **kwargs):
    return Field(
        input__attrs__type="range",
        input__attrs__min=min,
        input__attrs__max=max,
        input__template="widgets/range.html",
        **kwargs
    )
