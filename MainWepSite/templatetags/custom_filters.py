from django import template

register = template.Library()

@register.filter(name='has_attribute')
def has_attribute(variant, attribute_name):
    return variant.attributes.filter(attribute__name=attribute_name).exists()
