from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    request = context.get('request')
    if not request:
        return ''
        
    query_params = request.GET.copy()
    query_params[field] = value
    return query_params.urlencode()
