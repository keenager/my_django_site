from markdown import Markdown
from markdown.extensions.toc import TocExtension
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def mark(value):
    extentions = ['extra', 'nl2br', 'markdown_del_ins', 'toc', 'codehilite']
    config = {
        'toc': {
            'toc_class': 'toc card',
            'permalink': True
        },
    }
    md = Markdown(extensions=extentions, extension_configs=config)
    html = md.convert(value)
    return mark_safe(html)
