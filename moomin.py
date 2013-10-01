import os
import subprocess
import urllib
import cookielib
import urllib2
import htmlentitydefs
import re
from bs4 import BeautifulSoup

class Client():

    def __init__(self):
        rcfile = os.path.join(os.getenv("HOME"), ".moominrc")

        f = open(rcfile)
        content = f.read()
        base_url, user_name_and_pass = content.split(' ')
        self.username, self.password = user_name_and_pass.strip().split(':')
        f.close()

        self.base_url = base_url

        # Cookie
        cj = cookielib.CookieJar()
        cookiehandler = urllib2.HTTPCookieProcessor(cj)

        use_basic_auth = False
        p = re.compile('(https?://)(.*?):(.*?)@(.*?)$')
        m = p.match(base_url)
        if m:
            basic_auth_user = m.group(2)
            basic_auth_password = m.group(3)
            self.base_url = m.group(1) + m.group(4)

            # Basic Auth
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, self.base_url, basic_auth_user, basic_auth_password)

            use_basic_auth = True

        if use_basic_auth:
            authhandler = urllib2.HTTPBasicAuthHandler(passman)
            opener = urllib2.build_opener(authhandler, cookiehandler)
            urllib2.install_opener(opener)

    def GET(self, page_name):
        url = self.base_url + "/" + page_name
        response = urllib2.urlopen(url)
        the_page = response.read()
        return the_page

    def browse(self, page_name):
        url = self.base_url + "/" + page_name
        subprocess.call(['open', url])

    def POST(self, page_name, values):
        url = self.base_url + "/" + page_name
        data = urllib.urlencode(dict([k.encode('utf-8'),unicode(v).encode('utf-8')] for k,v in values.items()))
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        return the_page

    def get_page(self, pagename):
        self.GET(pagename)

    def login(self):
        loginpath = "/?action=login"
        values = {"name": self.username,
                  "password": self.password,
                  "login": "Login"}

        self.POST(loginpath, values)

    def get_text(self, pagename):
        page = self.GET(pagename + "?action=edit&editor=text")
        soup = BeautifulSoup(page)
        return soup.find("textarea").string.encode('utf-8')

    def save_text(self, pagename, filename):
        page = self.GET(pagename + "?action=edit&editor=text")
        soup = BeautifulSoup(page)
        rev = soup.find("input", {"name": "rev"})['value']
        ticket = soup.find("input", {"name": "ticket"})['value']

        import codecs
        data = u''
        with codecs.open(filename, 'r', 'utf-8') as f:
            for line in f:
                data += line

        values = {
            'action': 'edit',
            'rev': rev,
            'ticket': ticket,
            'button_save': 'Save+Changes',
            'editor': 'text',
            'savetext': data,
            'comment': '',
            'category': '',
        }

        self.POST(pagename, values)

    def HTMLEntitiesToUnicode(self, text):
        """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
        text = BeautifulSoup(text, convertEntities=BeautifulSoup.HTML_ENTITIES)
        import HTMLParser
        h = HTMLParser.HTMLParser()
        return h.unescape(text)
