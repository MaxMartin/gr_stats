import requests
from datetime import datetime
import xml.etree.ElementTree as ET

class ForbiddenError(Exception):
    def __init__(self):
        self.message = "You're not allowed to do that!"

class NotFoundError(Exception):
    def __init__(self, user_id):
        self.message = "No user found with id " + user_id

def parse_date(review):
    """Parse a Goodreads timestamp into a datetime object.
    
    Args:
        review -- xml Element representing a GoodReads review
    
    Returns:
        A datetime object representing the time the book was marked as read.
    """

    return datetime.strptime(review.find('read_at').text,
        "%a %b %d %H:%M:%S %z %Y")

def num_pages(review):
    """Find the number of pages for a book in a Goodreads review.

    Args:
        review -- xml Element representing a GoodReads review

    Returns:
        An integer representing the number of pages in the book if a number
        is found; defaults to zero otherwise.
    """

    num = review.find('book').find('num_pages').text or 0
    return int(num)

def month_histogram(read_dates, pages=False):
    """Build a histogram of how much a user has read in each month.

    Args:
        read_dates -- a list of (datetime, int) tuples representing the number
            of pages read on a given day.
        pages (optional) -- specify whether the histogram should count pages
            read rather than books. Defaults to False.

    Returns:
        A list of twelve integers indicating the number of books or pages read
        in each month, depending on the value of the pages argument.
    """

    result = [0] * 12

    for date, num_pages in read_dates:
        if pages:
            result[date.month - 1] += num_pages
        else:
            result[date.month - 1] += 1

    return result

class DataBuilder:
    """Fetches information on books a user has read from the GoodReadsAPI."""

    # goodreads API key
    GR_KEY = "loljk"

    def __init__(self, user_id, fetch=False):
        """Sets user ID, optionally fetches data.

        By default, creating the DataBuilder will only set the ID property
        and will wait for an explicit instruction to fetch the data.

        Args:
            user_id -- the ID of the goodreads user data will be fetched for.
            fetch (optional) -- specify True to fetch data on initialization.
        """

        self.user_id = user_id
        self.reviews = []
        self.read_dates = []
        if fetch:
            self.fetch()

    def fetch(self):
        """Fetches data on books user has read from Goodreads API.
        
        Sets four properties on the object:
        reviews -- a list of xml elements representing books the user has read
        read_dates -- a list of (datetime, int) tuples representing the number
            of pages read on a given day.
        book_histogram -- a list of 12 integers representing how many books 
            the user has read in each month.
        page_histogram -- a list of 12 integers representing how many pages 
            the user has read in each month.
        """
        
        payload = {'id': self.user_id,
                   'v': '2',
                   'per_page': '200',
                   'key': DataBuilder.GR_KEY,
                   'shelf': 'read'}

        r = requests.get("https://www.goodreads.com/review/list",
                         params=payload)

        if r.status_code == 403:
            raise ForbiddenError
        elif r.status_code == 404:
            raise NotFoundError(self.user_id)

        self.reviews = ET.fromstring(r.text)[1]

        self.read_dates = [(parse_date(r), num_pages(r))
            for r in self.reviews if r.find('read_at').text]

        self.book_histogram = month_histogram(self.read_dates)
        self.page_histogram = month_histogram(self.read_dates, pages=True)

