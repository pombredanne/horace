from horace.driver import Driver
from horace.agent import Agent
from horace.page import Page
from horace.module import Module
from horace.contentNode import element, content_module
import re

# def sel(context, selector=None, module=None):
#     return lambda context: context.getElementBySelector(selector)

class DuckDuckGoFormModule(Module):
    baseSelector = '#search_form_homepage'

    _content = {
        'input': element(selector='#search_form_input_homepage'),
        'select': element(selector='#bang'),
        'submit': element(selector='#search_button_homepage')
    }


class DuckDuckGoFooterModule(Module):
    baseSelector = '#footer_homepage'

    _content = {
        'title': element(selector='#footer_homepage_left')
    }


class DuckDuckGoHomePage(Page):
    url = 'https://www.duckduckgo.com'
    title = 'DuckDuckGo'

    _content = {
        'logo': element(selector='#logo_homepage_link'),
        'form': content_module(module=DuckDuckGoFormModule),
        'footer': content_module(module=DuckDuckGoFooterModule)
    }

    # def query(self, q):
    #     self.form.input.value(q)
    #     self.form.submit.click()


class DuckDuckGoSearchPage(Page):
    url = '^https://www.duckduckgo.com?q=' # TODO use regexp here in at()
    title = 'DuckDuckGo'

    _content = {
        'logo': element(selector='#logo_homepage_link', required=False),
        'links': element(selector='div[class="results_links_deep highlight_d2"]')
    }

    def at(self, title):
        return re.search('at DuckDuckGo$', title)


class DuckDuckGoAgent(Agent):

    def drive(self):
        searchTerm = 'deus ex machina'
        self.to_at(DuckDuckGoHomePage)
        self.page.form.input.value(searchTerm)
        self.page.form.submit.click()
        self.at(DuckDuckGoSearchPage)
        print 'Found %s links for "%s"' % (len(self.page.links), searchTerm)
        self.close()

driver = Driver({
    'driver': 'phantoms'
})
# Web pages
if __name__ == '__main__':
    DDG = DuckDuckGoAgent(driver)
    DDG.drive()

