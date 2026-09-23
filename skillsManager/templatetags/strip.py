from django import template

register = template.Library()


@register.filter('strip')
def strip(text, striptext):
    if isinstance(text, str):
        return text.replace(striptext, "")
    return False
