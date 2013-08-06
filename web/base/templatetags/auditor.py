from django import template
from math import ceil

register = template.Library()

@register.filter
def perc_of(value, total):
    try:
        return int(ceil(float(value) * 100.0 / float(total)))
    except ValueError:
        return 0
