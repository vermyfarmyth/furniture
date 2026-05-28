from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class RegisterViewTests(TestCase):
    def setUp(self):
        self.register_url = reverse('accounts:register')
        self.profile_url = reverse('accounts:profile')

    def test_register_creates_user_and_profile(self):
        response = self.client.post(
            self.register_url,
            {
                'username': 'new_user',
                'email': 'new_user@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertRedirects(response, reverse('core:home'))
        self.assertTrue(User.objects.filter(username='new_user').exists())
        user = User.objects.get(username='new_user')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_register_fails_with_duplicate_email(self):
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='StrongPass123!',
        )

        response = self.client.post(
            self.register_url,
            {
                'username': 'another_user',
                'email': 'existing@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.context['form'].errors)
        self.assertFalse(User.objects.filter(username='another_user').exists())

    def test_authenticated_user_is_redirected_from_register(self):
        user = User.objects.create_user(
            username='logged_in',
            email='logged_in@example.com',
            password='StrongPass123!',
        )
        self.client.force_login(user)

        response = self.client.get(self.register_url)

        self.assertRedirects(response, self.profile_url)


class AuthFlowTests(TestCase):
    def setUp(self):
        self.user_password = 'StrongPass123!'
        self.user = User.objects.create_user(
            username='auth_user',
            email='auth_user@example.com',
            password=self.user_password,
        )

    def test_user_can_login(self):
        response = self.client.post(
            reverse('accounts:login'),
            {'username': self.user.username, 'password': self.user_password},
        )

        self.assertRedirects(response, reverse('core:home'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_can_logout_via_post(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('accounts:logout'))

        self.assertRedirects(response, reverse('core:home'))
        self.assertFalse('_auth_user_id' in self.client.session)
