from django import template

register = template.Library()

@register.filter
def int_add(str1, str2):
    return int(str1) + int(str2)

@register.filter
def int_mul(str1, str2):
    return int(str1) * int(str2)

@register.filter
def int_div(low, high):
    try:
        result = round(low/high*100,1)
    except:
        result = 0
    return result