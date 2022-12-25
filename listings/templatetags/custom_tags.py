from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    filtered = context['request'].GET.copy()
    for i, j in kwargs.items():
        filtered[i] = j
    return filtered.urlencode()
