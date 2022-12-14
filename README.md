
# ShortLink

ShortLink is a URL shortening service where you enter a URL and it returns a short URL that redirects to the original URL.

Video Walkthrough: https://drive.google.com/file/d/1WtKeKqnzZ0RIxx_jtZ-HfykrjlzylDGS/view?usp=sharing

## Installation for Development

```bash
python3 -m venv dev_environ
source dev_environ/bin/activate
pip install -r requirements.txt
./run_dev.sh
```

## Installation for Deployment

Docker Required
```bash
./build.sh
./run.sh
```
`.run.sh` runs the container in interactive mode. 
    
## Running Tests

To run tests, run the following command

```bash
  python3 test.py
```


## API Reference


```http
  POST /encode
```
Creates a short url, takes the original URL as input

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `URL` | `string` | **Required**. URL Object |

---

```http
  POST /decode
```
Returns the original URL pair of short url, takes the short url as input

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `short_url`      | `string` | **Required**. ShortURL Object |

---

```http
  GET /redirect/{short_url}
```
Redirects short URL to original URL. Try it on browser

my-service.com/redirect/short_url --> URL

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `short_url`      | `string` | **Required**. ShortURL Object |

## Authors

- [@ArdaKaya](https://www.github.com/Arda13)

