from django import template

register = template.Library()


@register.filter
def spaceUnderscore(value):
    return value.replace(" ", "_")
