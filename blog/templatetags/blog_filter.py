from markdown import Markdown
from markdown.extensions.toc import TocExtension
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def mark(value):
    toc = TocExtension(toc_class='toc card', permalink=True)
    extentions = ['nl2br', 'fenced_code',
                  'markdown_del_ins', 'attr_list', toc, 'tables']
    md = Markdown(extensions=extentions)
    html = md.convert(value)
    return mark_safe(html)
