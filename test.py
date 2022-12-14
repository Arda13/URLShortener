import requests
import unittest

class Test(unittest.TestCase):

# Tests to succeed
	def test_encode(self):
		url = 'https://www.google.com'
		response = requests.post('http://localhost:8000/encode', json={'url': url})
		short_url = response.json()['short_url']
		self.assertEqual(response.status_code, 200)
		# 6 digit string expected
		self.assertEqual(len(response.json()['short_url']), 6)

		return short_url

	def test_decode(self):
		response = requests.post('http://localhost:8000/decode', json={'short_url': self.test_encode()})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['url'], 'https://www.google.com')

	def test_redirect(self):
		response = requests.get('http://localhost:8000/redirect/' + self.test_encode())
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.url, 'https://www.google.com')
		# 302s are often used to create temporary redirects, but, with the advent of HTTP 1.1, 307 has replaced it as a valid temporary redirect.
		self.assertEqual(response.history[0].status_code, 307)

# Tests to fail
	def test_encode_fail(self):
		url = 'www.google.com'
		response = requests.post('http://localhost:8000/encode', json={'url': url})
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['detail'], 'Not a valid URL')

	def test_decode_fail(self):
		response = requests.post('http://localhost:8000/decode', json={'short_url': '123456'})
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.json()['detail'], 'URL not found')

	def test_redirect_fail(self):
		response = requests.get('http://localhost:8000/redirect/123456')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.json()['detail'], 'URL not found')

if __name__ == '__main__':
	unittest.main()
