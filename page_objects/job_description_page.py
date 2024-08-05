from typing import Self

import allure
from playwright.sync_api import Locator, Page, expect

from page_objects.base_page import BasePage


class JobDescriptionPage(BasePage):
    BTN_APPLY: Locator = None
    MSG_FILE_FORMAT: str = '//span[@data-name="upload-cv"]//span'
    CHB_CONSENT: Locator = None
    MSG_ERRORS: str = '//div[@class="message-form-content"]//div'
    MSG_NAME: str = '//span[@data-name="your-name"]//span'
    MSG_EMAIL: str = '//span[@data-name="your-email"]//span'
    MSG_MOBILE: str = '//span[@data-name="your-number"]//span'
    MSG_MESSAGE: str = '//span[@data-name="your-message"]//span'

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.BTN_APPLY = page.get_by_role('button', name="Apply")
        self.CHB_CONSENT = page.locator('//input[@type="checkbox"][@id="adConsentChx"]')

    @allure.step('Check main sections')
    def assert_main_elements_present(self) -> Self:
        expect(self.page.get_by_role('heading', name='General description')).to_be_visible()
        expect(self.page.get_by_role('heading', name='Requirements')).to_be_visible()
        expect(self.page.get_by_role('heading', name='Responsibilities')).to_be_visible()
        expect(self.page.get_by_role('heading', name='What we offer')).to_be_visible()
        expect(self.page.get_by_role('button', name="Apply")).to_be_visible()
        return self

    @allure.step('Fill Apply form')
    def fill_apply_form(self, name: str, email: str, mobile: str) -> Self:
        self.page.get_by_label('Name').fill(name)
        self.page.get_by_label('Email').fill(email)
        self.page.get_by_label('Mobile').fill(mobile)
        return self

    @allure.step('Upload CV file')
    def upload_cv_file(self, file_path: str) -> Self:
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_label('Upload your CV').click()
            file_chooser = fc_info.value
        file_chooser.set_files(file_path)
        return self

    def assert_error_message(self, msg_locator: str, expected_msg: str) -> Self:
        self.assert_element_has_text(msg_locator, expected_msg)
        return self
