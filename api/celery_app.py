import os
from urllib.request import urlopen
from celery import Celery
from bs4 import BeautifulSoup
from db_session import session
from models import Url



CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='tasks.get_title')
def get_title(original_url: str) -> str:
    """
    Retrieves the title of a webpage given its original URL.
    Args:
        original_url (str): The original URL of the webpage.
    Returns:
        str: The title of the webpage.
    """
    try:
        html = urlopen(original_url)
        soup = BeautifulSoup(html, 'lxml')
        title = soup.title.string
        url = session.query(Url).filter(Url.original_url == original_url).first()
        if url:
            url.title = title
            session.commit()
    except Exception:
        title = ''

    return title
