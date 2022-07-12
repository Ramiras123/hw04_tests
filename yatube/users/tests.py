from django.test import TestCase, Client
from http import HTTPStatus


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self) -> None:
        self.guest_client = Client()

    def tests_urls_about_avaible(self):
        """Страницы из url httpstatus доступны всем пользователям."""
        urls_names_https_status = {
            '/auth/logout/': HTTPStatus.OK,
            '/auth/signup/': HTTPStatus.OK,
            '/auth/login/': HTTPStatus.OK,
            '/auth/password_change/': HTTPStatus.FOUND,
            '/auth/password_change_done/': HTTPStatus.FOUND,
            '/auth/password_reset/': HTTPStatus.OK,
            '/auth/password_reset/done/': HTTPStatus.OK,
            '/auth/reset/done/': HTTPStatus.OK
        }
        for address, httpstatus in urls_names_https_status.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, httpstatus)

    def test_urls_uses_correct_template(self):
        """url-адрес использует соответсвующий шаблон"""
        templates_url_names = {
            'users/logged_out.html': '/auth/logout/',
            'users/login.html': '/auth/login/',
            'users/password_reset_form.html': '/auth/password_reset/',
            'users/password_reset_done.html': '/auth/password_reset/done/',
            'users/password_reset_complete.html': '/auth/reset/done/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                self.assertTemplateUsed(response, template)
