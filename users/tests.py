import json
from django.test import TestCase, Client
from .models import User


class RefreshEndpointTests(TestCase):
	def setUp(self):
		self.email = 'alice@example.com'
		self.password = 's3cr3tpass'
		self.username = 'alice'
		self.user = User.objects.create_user(
			username=self.username,
			email=self.email,
			password=self.password,
			name='Alice'
		)

	def test_cookie_based_refresh(self):
		client = Client()
		# Login to set the httponly refresh cookie
		login_payload = json.dumps({'email': self.email, 'password': self.password})
		resp = client.post('/api/users/login', login_payload, content_type='application/json')
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertIn('access', data)

		# Ensure the refresh cookie was set on the client
		cookie = client.cookies.get('refresh_token')
		self.assertIsNotNone(cookie)

		# Call refresh endpoint without body; cookie should be sent automatically
		resp2 = client.post('/api/users/refresh', content_type='application/json')
		self.assertEqual(resp2.status_code, 200)
		self.assertIn('access', resp2.json())

	def test_body_fallback_refresh(self):
		client = Client()
		# Login to get a refresh token cookie value
		login_payload = json.dumps({'email': self.email, 'password': self.password})
		resp = client.post('/api/users/login', login_payload, content_type='application/json')
		self.assertEqual(resp.status_code, 200)
		cookie = client.cookies.get('refresh_token')
		self.assertIsNotNone(cookie)
		refresh_value = cookie.value

		# Use a fresh client without cookies and send refresh in the body
		client2 = Client()
		body = json.dumps({'refresh': refresh_value})
		resp3 = client2.post('/api/users/refresh', body, content_type='application/json')
		self.assertEqual(resp3.status_code, 200)
		self.assertIn('access', resp3.json())

