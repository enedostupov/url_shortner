import hashlib
from flask import Flask, request, abort
from models import Url
from worker import celery
from db_session import session

BASE_URL = 'https://localhost:3000/'
SHORT_URL_LENGTH = 6
URLS_LIMIT = 10


app = Flask(__name__)


def generate_short_url(url: str) -> str:
    """
    Generate a short URL based on the given URL.
    Parameters:
        url (str): The original URL to generate a short URL for.
    Returns:
        str: The generated short URL.
    """

    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:SHORT_URL_LENGTH]


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """
    Shortens a given URL and saves it in the database.
    Returns:
        A dictionary containing the shortened URL.
    """

    original_url = request.json['url']
    url = session.query(Url).filter(Url.original_url == original_url).first()
    if not url:
        short_url = generate_short_url(original_url)
        url = Url(original_url=original_url, short_url=short_url)
        session.add(url)
        session.commit()
        celery.send_task('tasks.get_title', args=[original_url])

    return {'short_url': BASE_URL + url.short_url}


@app.route('/<shorten_url>')
def retrive_url(shorten_url: str):
    """
    Retrieve the original URL associated with a given shortened URL.
    Args:
        shorten_url (str): The shortened URL to retrieve the original URL for.
    Returns:
        dict: A dictionary containing the original URL.
    Raises:
        404: If the shortened URL does not exist in the database.
    """

    url = session.query(Url).filter(Url.short_url == shorten_url).first()
    if not url:
        abort(404)

    url.count += 1
    session.commit()
    return {'original_url': url.original_url}


@app.route('/top_urls')
def retrive_top_urls():
    """
    Retrieves the top URLs based on their count in descending order.
    Returns:
        A list of dictionaries containing the original URL, count, and title of each URL.
    """

    urls = session.query(Url).order_by(Url.count.desc()).limit(URLS_LIMIT).all()
    response = []
    for url in urls:
        response.append(
            {'original_url': url.original_url, 'count': url.count, 'title': url.title},
        )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')
