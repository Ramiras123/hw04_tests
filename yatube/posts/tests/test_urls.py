from django.test import TestCase, Client
from ..models import Post, User, Group
from http import HTTPStatus


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.not_author = User.objects.create_user(username='test_client')
        cls.group = Group.objects.create(
            title='test_title',
            slug='test_slug'
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.not_author)
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.author)
        self.post = Post.objects.create(
            text='test text',
            author=self.author,
            group=self.group
        )

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_avaible_all_user(self):
        """Страницы из url httpstatus доступны всем пользователям."""
        url_names_https_status = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.author.username}': HTTPStatus.OK,
            '/unexciting_page/': HTTPStatus.NOT_FOUND
        }
        for address, httpstatus in url_names_https_status.items():
            with self.subTest(adress=address):
                response = self.authorized_client.get(address, follow=True)
                self.assertEqual(response.status_code, httpstatus)

    def test_pages_uses_correct_templates(self):
        """url-адрес использует соответсвующий шаблон"""
        templates_url_names = {
            '/': 'posts/index.html',
            '/create/': 'posts/create_post.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.author.username}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client_author.get(address,
                                                      follow=True)
                self.assertTemplateUsed(response, template)

    def test_redirect_anonymous(self):
        """Перенаправление незарегистрированного
        пользователя на страницу авторизации из url redirect"""
        self.assertRedirects(
            self.guest_client.get(f'/posts/{self.post.id}/edit/'),
            '/auth/login/' + '?next=' + f'/posts/{self.post.id}/edit/')
        self.assertRedirects(
            self.guest_client.get('/create/'),
            '/auth/login/' + '?next=' + '/create/')
