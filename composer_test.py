import unittest
import composer


class StylerStub:
    def style(self, tag):
        pass


class TestComposer(unittest.TestCase):

    def test_compose_basic(self):
        article = {
            "title": "title",
            "subtitle": "subtitle",
            "paragraphs": [
                {
                    "type": "P",
                    "text": "This is a testing paragraph",
                    "markups": []
                }
            ]
        }
        result = composer.compose(article, lambda i: '', StylerStub(), None, [])
        expected = {
            "title": "title",
            "subtitle": "subtitle",
            "content": "<div><p>This is a testing paragraph</p></div>"
        }
        self.assertEqual(result, expected)

    def test_compose_with_single_markup(self):
        article = {
            "title": "title",
            "subtitle": "subtitle",
            "paragraphs": [
                {
                    "type": "P",
                    "text": "This is a testing paragraph",
                    "markups": [
                        {
                            "type": "STRONG",
                            "start": 5,
                            "end": 7
                        }
                    ]
                }
            ]
        }
        result = composer.compose(article, lambda i: '', StylerStub(), None, [])
        expected = {
            "title": "title",
            "subtitle": "subtitle",
            "content": "<div><p>This <strong>is</strong> a testing paragraph</p></div>"
        }
        self.assertEqual(result, expected)

    def test_compose_with_multiple_markups(self):
        article = {
            "title": "title",
            "subtitle": "subtitle",
            "paragraphs": [
                {
                    "type": "P",
                    "text": "This is a testing paragraph",
                    "markups": [
                        {
                            "type": "STRONG",
                            "start": 5,
                            "end": 7
                        },
                        {
                            "type": "EM",
                            "start": 10,
                            "end": 17
                        }
                    ]
                }
            ]
        }
        result = composer.compose(article, lambda i: '', StylerStub(), None, [])
        expected = {
            "title": "title",
            "subtitle": "subtitle",
            "content": "<div><p>This <strong>is</strong> a <i>testing</i> paragraph</p></div>"
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
