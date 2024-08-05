from typing import Self

import allure
from playwright.sync_api import Page

from page_objects.base_page import BasePage
from page_objects.job_description_page import JobDescriptionPage


class CheckPositionsPage(BasePage):
    POSITION_ITEM = '//div[@class="card-container"]//a'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @allure.step('Set position location')
    def set_location(self, location: str) -> Self:
        self.page.locator("#get_location").select_option(location)
        self.page.wait_for_load_state()
        self.page.wait_for_load_state('networkidle')
        print(f'\n{'':=<7}Location: {location} {'':=<7}')
        return self

    def _get_all_positions(self):
        all_positions = self.page.locator(self.POSITION_ITEM).all()
        self.page.wait_for_load_state()
        self.page.wait_for_load_state('networkidle')
        return all_positions

    @allure.step('Print all available positions to console')
    def print_all_positions(self) -> Self:
        all_positions = self._get_all_positions()
        if len(all_positions) == 0:
            print('There are no opened positions in the location')
        else:
            for position in all_positions:
                print(
                    f'Position: {position.locator('//h2').text_content()}\n',
                    f'More info: {position.get_attribute('href')}\n',
                    f'{'':=<15}\n')
        return self

    @allure.step('Open position with index {index}')
    def get_position_by_index(self, index: int) -> JobDescriptionPage:
        all_positions = self._get_all_positions()
        all_positions[index].click()
        return JobDescriptionPage(self.page)
