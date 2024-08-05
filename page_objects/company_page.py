from typing import Self

import allure
from playwright.sync_api import Page

from page_objects.base_page import BasePage
from page_objects.fb_page import FacebookPage


class CompanyPage(BasePage):
    SECTION_COMPANY_MEMBERS = '//section[@class="company-members"]'
    BTN_FACEBOOK = '//span[@class="musala musala-icon-facebook"]/..'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @allure.step('Open Facebook page')
    def get_company_facebook_page(self) -> Self:
        with self.page.context.expect_page() as facebook_page_info:
            self.page.locator(self.BTN_FACEBOOK).click()
            return FacebookPage(facebook_page_info.value)
