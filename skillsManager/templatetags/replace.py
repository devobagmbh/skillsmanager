from django import template

register = template.Library()


@register.filter
def replace(value, args):
    """Usage: {{ value|replace:"old,new" }} or with variables via string concatenation."""
    try:
        old, new = args.split(',')
        return value.replace(old, new)
    except ValueError:
        return value  # fallback if args is malformed
