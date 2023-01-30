from django import template
register = template.Library()

@register.inclusion_tag('block/validate.html')
def validate_tag(form):
    return { 'errors': form.errors, 'form': form }

