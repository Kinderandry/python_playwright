from typing import Self

from playwright.sync_api import Page

from page_objects.careers_page import CareersPage
from page_objects.company_page import CompanyPage


class NavigationMenu:
    MENU_ITEM = '//div[@id="menu"]//a[text()="{}"]'

    def __init__(self, page: Page) -> None:
        self.page = page

    def _navigate_menu(self, menu_item: str) -> Self:
        self.page.locator(self.MENU_ITEM.format(menu_item)).dispatch_event('click')
        return self

    def get_careers_page(self) -> CareersPage:
        self._navigate_menu('Careers')
        return CareersPage(self.page)

    def get_company_page(self) -> CompanyPage:
        self._navigate_menu('Company')
        return CompanyPage(self.page)

    def get_services_page(self) -> None:
        self._navigate_menu('Services')
        raise NotImplementedError

    def get_clients_page(self) -> None:
        self._navigate_menu('Clients')
        raise NotImplementedError

    def get_community_page(self) -> None:
        self._navigate_menu('Community')
        raise NotImplementedError

    def get_legal_page(self) -> None:
        self._navigate_menu('Legal')
        raise NotImplementedError
