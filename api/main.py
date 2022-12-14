import validators
from utils.utils import *

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from models.models import URL, ShortURL
from starlette import status

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler

urls = {}

limiter = Limiter(key_func=get_ip)
# 10 requests per minute
call_freq = "10/minute"
app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get('/')
async def index():
	return {'message': 'Welcome to the URL Shortner API'}


@app.post('/encode', response_model=ShortURL)
@limiter.limit(call_freq)
async def encode(request: Request, url: URL):
	# parse the url to check if it is valid
	if not validators.url(url.url):
	# if the url is not valid, raise an exception
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not a valid URL')
	else:
		if url.url in urls.values():
			# If the URL is already in the dictionary, return the key
			for key, value in urls.items():
				if value == url.url:
					return ShortURL(short_url=key, status_code=status.HTTP_200_OK)
		else:
			# Generate a random string
			short_url = random_string(6)
			# Add the URL to the dictionary
			urls[short_url] = url.url
			return ShortURL(short_url=short_url, status_code=status.HTTP_201_CREATED)


@app.post('/decode', response_model=URL)
@limiter.limit(call_freq)
async def decode(request: Request, short_url: ShortURL):
	# Get the URL from the dictionary return jsonify the URL
	if len(short_url.short_url) == 6:
		if short_url.short_url in urls:
			url = urls[short_url.short_url]
			return URL(url=url, status_code=status.HTTP_200_OK)
		else:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='URL not found')
	else:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='URL must be 6 characters long to decode')

# Dynamic URL inputs are dangerous, be sure to validate the input
@app.get('/redirect/{short_url}', status_code=status.HTTP_307_TEMPORARY_REDIRECT, response_class=RedirectResponse)
@limiter.limit(call_freq)
async def redirect(request: Request, short_url: str):
	# in this case, the short_url must be 6 characters long
	if len(short_url) == 6:
		if short_url in urls:
			url = urls[short_url]
			return RedirectResponse(url=url)
		else:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='URL not found')
	else:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid short URL, must be 6 characters long')