import copy
class Url:
    def __init__(self, scheme=None, authority=None, path=None, query=None, fragment=None):
        self.scheme = scheme
        self.authority = authority
        self.path = path
        self.query = query
        self.fragment = fragment

    def __str__(self):
        path = '' if self.path is None else f'/{"/".join(self.path)}'
        query = '' if self.query is None or self.query == dict() else f'?{"&".join(f"{x}={y}" for x, y in self.query.items())}'
        fragment = '' if self.fragment is None else f''
        return f'{self.scheme}://{self.authority}{path}{query}{fragment}'

    def __eq__(self, obj: object):
        return str(self) == str(obj)


class HttpsUrl(Url):
    def __init__(self, scheme=None, authority=None, path=None, query=None, fragment=None):
        super().__init__('https', authority, path, query, fragment)


class HttpUrl(Url):
    def __init__(self, scheme=None, authority=None, path=None, query=None, fragment=None):
        super().__init__('http', authority, path, query, fragment)


class GoogleUrl(HttpsUrl, Url):
    def __init__(self, scheme=None, authority=None, path=None, query=None, fragment=None):
        super().__init__(scheme, 'google.com', path, query, fragment)


class WikiUrl(HttpsUrl, Url):
    def __init__(self, scheme=None, authority=None, path=None, query=None, fragment=None):
        super().__init__(scheme, 'wikipedia.org', path, query, fragment)


class UrlCreator(Url):
    def __init__(self, scheme=None, authority=None, path=None, query=None, fragment=None):
        super().__init__(scheme, authority, path, query, fragment)

    def __getattr__(self, attr):
        self.path = [attr] if self.path is None else self.path + [attr]
        return self

    def __call__(self, *args, **kwds):
        tmp_args = copy.deepcopy(args)
        if tmp_args:
            self.path = [p for p in tmp_args]

        tmp_keys = copy.deepcopy(kwds)
        self.query = {k: v for k, v in tmp_keys.items()}
        return self

    def _create(self):
        return str(self)

# ===== part 1 =====
assert GoogleUrl() == HttpsUrl(authority='google.com')
assert GoogleUrl() == Url(scheme='https', authority='google.com')
assert GoogleUrl() == 'https://google.com'
assert WikiUrl() == str(Url(scheme='https', authority='wikipedia.org'))
assert WikiUrl(path=['wiki', 'python']) == 'https://wikipedia.org/wiki/python'
assert GoogleUrl(query={'q': 'python', 'result': 'json'}) == 'https://google.com?q=python&result=json'


# ===== part 2 =====
url_creator = UrlCreator(scheme='https', authority='docs.python.org')
assert url_creator.docs.v1.api.list == 'https://docs.python.org/docs/v1/api/list'
assert url_creator('api','v1','list') == 'https://docs.python.org/api/v1/list'
assert url_creator('api','v1','list', q='my_list') == 'https://docs.python.org/api/v1/list?q=my_list'
assert url_creator('3').search(q='getattr', check_keywords='yes', area='default')._create() == 'https://docs.python.org/3/search?q=getattr&check_keywords=yes&area=default'
