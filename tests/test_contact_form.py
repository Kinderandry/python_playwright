import json

import pytest
from playwright.sync_api import Page, expect

from page_objects.main_page import MainPage


def json_test_data():
    with open('test_data/emails.json', 'r') as f:
        for item in json.loads(f.read()):
            yield item.get('email')


class TestMusalaSite:
    @pytest.fixture(scope="function", autouse=True)
    def before_each(self, page: Page):
        page.goto('http://www.musala.com/')
        yield

    @pytest.mark.parametrize('email', json_test_data())
    def test_contact_form_email_verification(self, page: Page, email):
        page.click('//button[contains(@class, "contact")]')

        page.get_by_label('Name').fill('Test')
        page.get_by_label('Email').fill(email)
        page.get_by_label('Mobile').fill('+3590000000')
        page.get_by_label('Subject').fill('Test Subject')
        page.get_by_label('Your Message').fill('Lorem ipsum')

        expect(page.locator('//span[@data-name="your-email"]//span')).to_have_text('The e-mail address entered is invalid.')

    def test_facebook_profile(self, page: Page):
        page.click('//a[@data-cli_action="accept_all"]')

        page.locator('//div[@id="menu"]//a[text()="Company"]').dispatch_event('click')

        expect(page).to_have_url('https://www.musala.com/company/')
        expect(page.locator('//section[@class="company-members"]')).to_be_visible()
        with page.context.expect_page() as facebook_page_info:
            page.locator('//span[@class="musala musala-icon-facebook"]/..').click()
            facebook_page = facebook_page_info.value

        expect(facebook_page).to_have_url('https://www.facebook.com/MusalaSoft?fref=ts')
        facebook_page.locator('//div[@aria-label="Decline optional cookies" and  not(@aria-disabled="true")]').click()
        facebook_page.locator('//div[@aria-label="Close"]').click()
        # facebook_page.locator('//*[local-name() = "svg"][@aria-label="Musala Soft"][@role="img"][1]').all()[0].screenshot(path='screenshot_AR.png')
        # with open('screenshot.png', 'rb') as screenshot_ER:
        #     with open('screenshot_AR.png', 'rb') as screenshot_AR:
        #         assert screenshot_ER == screenshot_AR

        # expect(facebook_page.locator('//*[local-name() = "svg"][@aria-label="Musala Soft"][@role="img"]')).to_be_visible()

    def test_careers_page_send_cv(self, page: Page):
        page.locator('//div[@id="menu"]//a[text()="Careers"]').dispatch_event('click')
        page.get_by_role("button", name="Check our open positions").click()
        page.locator("#get_location").select_option("Anywhere")
        expect(page).to_have_url("https://www.musala.com/careers/join-us/?location=Anywhere")
        page.get_by_role("link", name="Senior Automation QA Engineer").click()
        expect(page.get_by_role('heading', name='General description')).to_be_visible()
        expect(page.get_by_role('heading', name='Requirements')).to_be_visible()
        expect(page.get_by_role('heading', name='Responsibilities')).to_be_visible()
        expect(page.get_by_role('heading', name='What we offer')).to_be_visible()
        expect(page.get_by_role('button', name="Apply")).to_be_visible()
        page.get_by_role('button', name="Apply").click()

        page.get_by_label('Name').fill('')
        page.get_by_label('Email').fill('test@test')
        page.get_by_label('Mobile').fill('test')

        with page.expect_file_chooser() as fc_info:
            page.get_by_label("Upload your CV").click()
            file_chooser = fc_info.value

        file_chooser.set_files("test_data/emails.json")
        expect(page.locator('//span[@data-name="upload-cv"]//span')).to_have_text('You are not allowed to upload files of this type.')

        page.locator('//input[@type="checkbox"][@id="adConsentChx"]').click()
        page.get_by_role('button', name="Send").click()
        expect(page.locator('//div[@class="message-form-content"]//div')).to_have_text(
            'One or more fields have an error. Please check and try again.')
        page.get_by_role('button', name="Close").click()

        expect(page.locator('//span[@data-name="your-name"]//span')).to_have_text('The field is required.')
        expect(page.locator('//span[@data-name="your-email"]//span')).to_have_text('The e-mail address entered is invalid.')
        expect(page.locator('//span[@data-name="mobile-number"]//span')).to_have_text('The telephone number is invalid.')
        expect(page.locator('//span[@data-name="your-message"]//span')).to_have_text('The field is required.')

    @pytest.mark.parametrize('location', ('Sofia', 'Skopje', 'Anywhere'))
    def test_careers_page_open_positions(self, page: Page, location):
        check_positions_page = (MainPage(page)
                                .get_careers_page()
                                .get_check_positions_page())
        page.get_by_role("button", name="Check our open positions").click()
        page.locator("#get_location").select_option(location)
        page.wait_for_load_state()
        all_positions = page.locator('//div[@class="card-container"]//a').all()

        print(f'\n{'':=<7}Location: {location} {'':=<7}')
        if len(all_positions) == 0:
            print(f'There are no opened positions in {location}')
        else:
            for position in all_positions:
                print(
                    f'Position: {position.locator('//h2').text_content()}\n',
                    f'More info: {position.get_attribute('href')}\n',
                    f'{'':=<15}\n')
