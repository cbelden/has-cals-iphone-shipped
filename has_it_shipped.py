from flask import Flask, render_template
from bs4 import BeautifulSoup
from datetime import datetime
import urllib2
import hashlib
import os


app = Flask(__name__)

@app.route('/')
def index():
    """Returns/Renders the home (only) page."""
    has_changed = 'yes' if status_has_changed() else 'no'
    return render_template('index.html', has_it_shipped=has_changed)


def status_has_changed():
    """
    Returns true if the md5 hash of order_html does not match the md5 hash stored in the shipping info hash file.
    """

    # Get the previous hash
    old_hash = os.environ["OLD_STATUS_HASH"]

    # Construct the new hash
    order_html = get_order_info_html()
    new_hash = hashlib.md5(order_html).hexdigest()

    # Log new hash
    print str(datetime.now), new_hash

    # Return  true if the hashes are different
    return old_hash != new_hash


def get_order_info_html():
    """
    Retrieves the html for my iphone's order status from 
    """

    # This is the order status url from my Verizon email
    order_status_url = os.environ['STATUS_URL'];
    
    # Set user agent to the default User-agent in Chrome (Verizon blocks urllib2's default user agent)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]
    
    # Get the order page
    order_page = opener.open(order_status_url).read()

    # Soup that shit up
    soup = BeautifulSoup(order_page)

    # Get the table that contains the shipping information
    return str(soup.select("div.contentContainerNoHead"))

if __name__ == '__main__':
    app.run()
