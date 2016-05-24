__author__ = 'yoshi.miyamoto'

from django import template

register = template.Library()

@register.filter
def field_type(obj):
    name = obj.__class__.__name__
    return name


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

