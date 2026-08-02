from django.test import TestCase
from django.urls import reverse
from .models import User, UserProfile


class UserAuthAndProfileTests(TestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "SecurePass123!"
        self.name = "Test User"
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            name=self.name,
        )

    def test_user_profile_automatically_created(self):
        """Verify that UserProfile is automatically created via signal upon User creation."""
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
        self.assertEqual(self.user.profile.user, self.user)

    def test_login_redirects_authenticated_user_to_dashboard(self):
        """Authenticated users visiting login should be redirected to dashboard, preventing redirect loop."""
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_signup_creates_user_and_profile_and_redirects_to_dashboard(self):
        """New signup creates User and UserProfile, logging in and redirecting to dashboard."""
        new_email = "newuser@example.com"
        response = self.client.post(reverse('signup'), {
            'name': 'New User',
            'email': new_email,
            'password': 'NewPassword123!',
        })
        self.assertRedirects(response, reverse('dashboard'))
        new_user = User.objects.get(email=new_email)
        self.assertTrue(UserProfile.objects.filter(user=new_user).exists())

    def test_protected_views_require_authentication(self):
        """Unauthenticated requests to profile and onboarding should redirect to login."""
        profile_response = self.client.get(reverse('profile'))
        self.assertRedirects(profile_response, f"{reverse('login')}?next={reverse('profile')}")

        onboarding_response = self.client.get(reverse('onboarding'))
        self.assertRedirects(onboarding_response, f"{reverse('login')}?next={reverse('onboarding')}")

    def test_onboarding_view_get_and_post_submission(self):
        """Authenticated user can submit onboarding form and persist profile details."""
        self.client.login(email=self.email, password=self.password)

        get_response = self.client.get(reverse('onboarding'))
        self.assertEqual(get_response.status_code, 200)

        post_data = {
            'name': 'Updated Test Name',
            'date_of_birth': '1995-06-15',
            'bio': 'Lover of mindful eating',
            'current_weight': '70.5',
            'goal_weight': '65.0',
            'weight_unit': 'kg',
            'height_metric': '175',
            'height_unit': 'cm',
            'activity_level': 'Moderately Active',
            'dietary_style': 'Vegetarian',
            'triggers': ['Stress', 'Boredom'],
        }

        post_response = self.client.post(reverse('onboarding'), post_data)
        self.assertRedirects(post_response, reverse('dashboard'))

        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()

        self.assertEqual(self.user.name, 'Updated Test Name')
        self.assertEqual(str(self.user.profile.date_of_birth), '1995-06-15')
        self.assertEqual(self.user.profile.bio, 'Lover of mindful eating')
        self.assertEqual(self.user.profile.current_weight, 70.5)
        self.assertEqual(self.user.profile.goal_weight, 65.0)
        self.assertEqual(self.user.profile.height, 175.0)
        self.assertEqual(self.user.profile.preferences['activity_level'], 'Moderately Active')
        self.assertEqual(self.user.profile.preferences['dietary_style'], 'Vegetarian')
        self.assertEqual(self.user.profile.preferences['triggers'], ['Stress', 'Boredom'])

