from typing import Self

import allure
from playwright.sync_api import Page, expect

from page_objects.base_page import BasePage
from page_objects.navigation_menu import NavigationMenu


class MainPage(BasePage):
    BTN_CONTACT_US = '//button[contains(@class, "contact")]'

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.navigation_menu = NavigationMenu(page)

    @allure.step('Open contact form')
    def get_contact_us(self) -> Self:
        self.page.locator(self.BTN_CONTACT_US).click()
        return self

    @allure.step('Fill contact form with data: name {name}, email {email}, mobile {mobile}, subject {subject}, msg {msg}')
    def fill_contact_form(self, name: str, email: str, mobile: str, subject: str, msg: str) -> Self:
        self.page.get_by_label('Name').fill(name)
        self.page.get_by_label('Email').fill(email)
        self.page.get_by_label('Mobile').fill(mobile)
        self.page.get_by_label('Subject').fill(subject)
        self.page.get_by_label('Your Message').fill(msg)

        self.page.locator('//input[@type="checkbox"][@id="adConsentChx"]').click()
        self.page.get_by_role('button', name="Send").click()
        return self

    @allure.step('Check error message')
    def assert_error_message(self, error_message: str) -> Self:
        expect(self.page.locator('//span[@data-name="your-email"]//span')).to_have_text(error_message)
        return self
