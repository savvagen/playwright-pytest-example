import json


class Article:
    def __init__(self, title=None, subject=None, body=None, tags=None, comment=None):
        self.title = title
        self.subject = subject
        self.body = body
        self.comment = comment
        self.tags = tags

    def __str__(self):
        return json.dumps(self.__dict__)


def fake_article():
    art = Article(
        title='Python Playwright Demo',
        subject='Playwright Demo',
        tags="test",
        body="\n# Hello World\n\nSome `text` \n\nSome function:\n```\ndef function():\n     pass\n```\n"
    )
    return art
