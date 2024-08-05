from playwright.sync_api import Locator, Page

from page_objects.base_page import BasePage
from page_objects.check_positions_page import CheckPositionsPage


class CareersPage(BasePage):
    BTN_CHECK_POSITIONS: Locator = None

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.BTN_CHECK_POSITIONS = self.get_button('Check our open positions')

    def get_check_positions_page(self) -> CheckPositionsPage:
        self.BTN_CHECK_POSITIONS.click()
        return CheckPositionsPage(self.page)
