from django import template
import math

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def abs(value):
    """Return the absolute value."""
    try:
        return math.fabs(float(value))
    except (ValueError, TypeError):
        return '' 