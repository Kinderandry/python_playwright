from typing import Self

import allure
from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def get_button(self, button_name: str) -> Locator:
        return self.page.get_by_role('button', name=button_name)

    @allure.step('Accept cookies')
    def accept_cookies(self) -> Self:
        self.page.click('//a[@data-cli_action="accept_all"]')
        return self

    @allure.step('Check current URL')
    def assert_current_url(self, expected_url: str) -> Self:
        expect(self.page).to_have_url(expected_url)
        return self

    @allure.step('Check if element is visible')
    def assert_element_visible(self, locator: str) -> Self:
        expect(self.page.locator(locator)).to_be_visible()
        return self

    @allure.step('Check if element has specific text')
    def assert_element_has_text(self, locator: str, text: str) -> Self:
        expect(self.page.locator(locator)).to_have_text(text)
        return self
