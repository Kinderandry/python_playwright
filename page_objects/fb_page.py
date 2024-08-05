from typing import Self

import allure
import requests
from playwright.sync_api import Page

from page_objects.base_page import BasePage


class FacebookPage(BasePage):
    BTN_DECLINE_COOKIES = '//div[@aria-label="Decline optional cookies" and  not(@aria-disabled="true")]'
    BTN_CLOSE_LOGIN = '//div[@aria-label="Close"]'
    IMG_COVER = '//img[@data-imgperflogname="profileCoverPhoto"]'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @allure.step('Decline cookies')
    def decline_cookies(self):
        self.page.wait_for_load_state()
        if self.page.locator(self.BTN_DECLINE_COOKIES).is_visible():
            self.page.locator(self.BTN_DECLINE_COOKIES).click()
        return self

    @allure.step('Close login window')
    def close_login(self):
        self.page.wait_for_load_state()
        self.page.locator(self.BTN_CLOSE_LOGIN).click()

    @allure.step('Download cover image')
    def download_cover_image(self, img_name: str) -> Self:
        profile_img = self.page.locator(self.IMG_COVER).get_attribute('src')
        img = requests.get(profile_img)
        with open(f'ER/{img_name}', 'wb') as f:
            f.write(img.content)
        return self

    @allure.step('Compare images')
    def compare_images(self, ar_img: str, er_img: str) -> Self:
        with open(f'ER/{er_img}', 'rb') as img_ER:
            with open(f'ER/{ar_img}', 'rb') as img_AR:
                assert img_ER.read() == img_AR.read()
        return self
