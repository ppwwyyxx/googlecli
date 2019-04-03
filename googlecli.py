#!/usr/bin/env python

from __future__ import print_function
import sys
import termios, fcntl, struct
import webbrowser
from bs4 import BeautifulSoup, SoupStrainer
import six
from six.moves.urllib.parse import quote_plus, parse_qs
from six.moves.http_client import HTTPSConnection
if six.PY2:
    from cStringIO import StringIO
else:
    from io import BytesIO as StringIO
import argparse

winsz = fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, "1234")
columns = struct.unpack("HH", winsz)[1]
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
    'accept-encoding': 'gzip'
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', help='start at the Nth result', type=int,
                       default=0)
    parser.add_argument('-n', '--number', help='show N results', type=int,
                       default=5)
    parser.add_argument('-l', '--language', help='search by language', default=None)
    parser.add_argument('--no-color',
                        help='disable color output', action='store_true')
    parser.add_argument('-o', '--open',
                        help='open the first result with browser (feeling lucky)',
                        action='store_true')
    parser.add_argument('-r', '--reverse', help='output in reversed order, to work with URL selecter in tmux/urxvt',
                       action='store_true')
    parser.add_argument('query', help='query', nargs='+')
    global args
    args = parser.parse_args()

def parse_google(html):
    # desktop version (work with user-agent set)
    ss = SoupStrainer('div', attrs={'class': 'rc'})
    # to speed up
    start = html.find(b'--a--') + 6
    end = html.find(b'--z--', start) - 2
    if start > 10 and end > start:
        html = html[start:end]

    #ss = SoupStrainer('li', attrs={'class': 'g'})  # plain version
    soup = BeautifulSoup(html, 'html.parser', parse_only=ss)

    def parse_item(item):
        a = item.find('a')
        url = a.attrs['href']
        # plain version url handling
        #if not url.startswith('/url'):
            #url = 'https:///google.com' + url
        #else:
            #url = parse_qs(url[5:])['q'][0]
        title = a.text
        st = item.find('span', attrs={'class': 'st'})
        text = st.text
        return url, title, text
    return [parse_item(i) for i in soup]

# from github:henux/cli-google
def print_entry(url, title, text):
    if not args.no_color:
        print("\x1B[96m* \x1B[92m%s\n\x1B[93m%s\x1B[39m" % (title, url))
    else:
        print("* %s\n%s" % (title, url))
    # Print the text with truncating.
    col = 0
    for w in text.split():
        if (col + len(w) + 1) > columns:
            col = 0
            print()
        print(w, end=' ')
        col += len(w) + 1
    print()
    print()

def main():
    parse_args()
    query = '+'.join([quote_plus(k) for k in args.query])

    # build URL
    url = "https://www.google.com/search?"
    if args.start != None:
        url += "start={}&".format(args.start)
    if args.number != None:
        # request more
        url += "num={}&".format(args.number + 2)
    if args.language != None:
        url += "hl={}&".format(args.language)
    url += "q={}".format(query)
    print(url)
    print()

    # connect
    conn = HTTPSConnection("www.google.com")
    conn.request("GET", url, headers=headers)
    resp = conn.getresponse()
    if resp.status != 200:
        print("Server responded with an error:", str(resp.status))
        sys.exit(1)
    html = resp.read()
    if resp.getheader('content-encoding') == 'gzip':
        import gzip
        data = StringIO(html)
        html = gzip.GzipFile(fileobj=data).read()

    # parse
    results = parse_google(html)[:args.number]
    if args.open:
        webbrowser.open(results[0][0])
    if args.reverse:
        results = reversed(results)
    for (url, title, text) in results:
        print_entry(url, title, text)
    conn.close()

if __name__ == '__main__':
    main()
