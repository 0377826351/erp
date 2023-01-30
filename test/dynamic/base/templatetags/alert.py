from django import template
register = template.Library()

@register.inclusion_tag('block/alert.html')
def alert_tag(type, message):
    return { 'type': type, 'message': message }

@register.inclusion_tag('block/flash_message.html')
def flash_message(messages):
    convert_msg_tags = {
        'info': 'info',
        'success': 'success',
        'warning': 'warning',
        'error': 'danger',
        'debug': 'danger'
    }
    result = {}
    for item in messages:
        tag = convert_msg_tags.get(item.tags)
        if tag not in result: result[tag] = []
        result[tag].append(item)
    return { 'messages': result }
