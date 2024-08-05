import json
import os

import allure
import pytest
import requests
from playwright.sync_api import Page

from page_objects.main_page import MainPage

TEST_DATA = os.path.dirname(__file__) + '/test_data/emails.json'


def json_test_data():
    with open(TEST_DATA, 'r') as f:
        for item in json.loads(f.read()):
            yield item.get('email')


class TestMusalaSite:
    @pytest.fixture(scope="function", autouse=True)
    def before_each(self, page: Page):
        allure.step('Open url')
        page.goto('')
        yield

    @allure.tag('main_page')
    @pytest.mark.parametrize('email', json_test_data())
    def test_contact_form_email_verification(self, page: Page, email):
        main_page = MainPage(page)
        main_page.get_contact_us()
        main_page.fill_contact_form(name='Test',
                                    email=email,
                                    mobile='+3590000000',
                                    subject='Test Subject',
                                    msg='Lorem ipsum')

        main_page.assert_error_message('The e-mail address entered is invalid.')

    @allure.tag('facebook')
    def test_facebook_profile(self, page: Page, base_url):
        main_page = MainPage(page)
        main_page.accept_cookies()
        company_page = main_page.navigation_menu.get_company_page()
        company_page.assert_current_url(f'{base_url}/company/')
        company_page.assert_element_visible(company_page.SECTION_COMPANY_MEMBERS)
        fb_page = company_page.get_company_facebook_page()

        fb_page.assert_current_url('https://www.facebook.com/MusalaSoft?fref=ts')
        fb_page.decline_cookies()
        fb_page.close_login()
        fb_page.download_cover_image('profile_cover_AR.jpg')

        fb_page.compare_images('profile_cover_AR.jpg', 'profile_cover_ER.jpg')

    @allure.tag('careers')
    def test_careers_page_send_cv(self, page: Page, base_url):
        check_positions_page = (MainPage(page)
                                .navigation_menu
                                .get_careers_page()
                                .get_check_positions_page())

        check_positions_page.set_location('Anywhere')
        check_positions_page.assert_current_url(f'{base_url}/careers/join-us/?location=Anywhere')

        jd_page = check_positions_page.get_position_by_index(0)
        jd_page.assert_main_elements_present()
        jd_page.BTN_APPLY.click()

        jd_page.fill_apply_form(name='',
                                email='test@test',
                                mobile='test')
        jd_page.upload_cv_file(TEST_DATA)
        jd_page.assert_element_has_text(jd_page.MSG_FILE_FORMAT,
                                        'You are not allowed to upload files of this type.')

        jd_page.CHB_CONSENT.click()
        jd_page.get_button('Send').click()
        jd_page.assert_element_has_text(jd_page.MSG_ERRORS, 'One or more fields have an error. Please check and try again.')
        jd_page.get_button('Close').click()

        jd_page.assert_element_has_text(jd_page.MSG_NAME, 'The field is required.')
        jd_page.assert_element_has_text(jd_page.MSG_EMAIL, 'The e-mail address entered is invalid.')
        jd_page.assert_element_has_text(jd_page.MSG_MOBILE, 'The telephone number is invalid.')
        jd_page.assert_element_has_text(jd_page.MSG_MESSAGE, 'The field is required.')

    @allure.tag('careers')
    @pytest.mark.parametrize('location', ('Sofia', 'Skopje', 'Anywhere'))
    def test_careers_page_open_positions(self, page: Page, location):
        check_positions_page = (MainPage(page)
                                .navigation_menu
                                .get_careers_page()
                                .get_check_positions_page())

        check_positions_page.set_location(location)
        check_positions_page.print_all_positions()
