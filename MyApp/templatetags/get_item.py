from django.template.defaulttags import register

@register.filter
def get_item(obj, key):
    try:
        return obj.get(key)
    except AttributeError:
        try:
            return obj[key]
        except (KeyError, IndexError, TypeError):
            return None
