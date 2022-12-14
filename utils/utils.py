import os
from fastapi import Request
import base64
import hashlib

def get_ip(request: Request):
	if "X-Forwarded-For" in request.headers:
		return request.headers["X-Forwarded-For"]
	else:
		return request.client.host

def random_string(length):
	return base64.urlsafe_b64encode(hashlib.sha256(os.urandom(256)).digest()).decode('utf-8')[:length]

