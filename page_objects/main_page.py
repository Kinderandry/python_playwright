from typing import Self

from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def get_button(self, button_name: str) -> Locator:
        return self.page.get_by_role('button', name=button_name)


class CompanyPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)


class CheckPositionsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)


class CareersPage(BasePage):
    BTN_CHECK_POSITIONS: Locator = None

    class Btn:
        CHECK_POSITIONS: Locator = None

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.Btn.CHECK_POSITIONS = self.get_button('Check our open positions')

    def get_check_positions_page(self) -> CheckPositionsPage:
        self.Btn.CHECK_POSITIONS.click()
        return CheckPositionsPage(self.page)


class MainPage(BasePage):
    MENU_ITEM = '//div[@id="menu"]//a[text()="{}"]'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate_menu(self, menu_item: str) -> Self:
        self.page.locator(self.MENU_ITEM.format(menu_item)).dispatch_event('click')
        return self

    def get_careers_page(self) -> CareersPage:
        self.navigate_menu('Careers')
        return CareersPage(self.page)
