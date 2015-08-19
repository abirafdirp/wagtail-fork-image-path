from django.template.loader import render_to_string
import re


class Sitemap(object):
    template = 'wagtailsitemaps/sitemap.xml'

    def __init__(self, site):
        self.site = site

    def get_pages(self):
        return self.site.root_page.get_descendants(inclusive=True).live().public().order_by('path')

    def get_urls(self):
        for page in self.get_pages():
            for url in page.specific.get_sitemap_urls():
                url['location'] = re.sub(r'(_page)', '', url['location'])
                yield url

    def render(self):
        return render_to_string(self.template, {
            'urlset': self.get_urls()
        })
