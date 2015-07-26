# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# pytter
# copyright (c) 2015 Vincent Loy
# Vincent Loy <vincent.loy1@gmail.com>

import unittest
import pprint
from pytter import Pytter

# p = Pytter('i\'m a super #tweet about no more no sense #cool @pastaws')
#
# print(p.hashtags)

pp = pprint.PrettyPrinter()
HTML_URL_FORMAT = '<a href="{url}" target="_blank" class="{html_class}">{text}</a>'


class PytterTests(unittest.TestCase):
    def test_urls(self):
        t0 = Pytter('tweet url https://github.com/VincentLoy/pytter/blob/master/pytter/pytter.py, #url')
        t1 = Pytter('tweet url https://github.com/VincentLoy/pytter/blob/master/pytter/pytter.py, '
                    + 'http://google.com #url')

        self.assertEqual(t0.urls[0].get('url'), 'https://github.com/VincentLoy/pytter/blob/master/pytter/pytter.py')
        self.assertEqual(t1.urls[0].get('url'), 'https://github.com/VincentLoy/pytter/blob/master/pytter/pytter.py')
        self.assertEqual(t1.urls[1].get('html'), HTML_URL_FORMAT.format(url='http://google.com',
                                                                        text='http://google.com',
                                                                        html_class=t1.get_html_classes().get('url')))

    def test_users(self):
        t0 = Pytter('this is a tweet for @nano @pastaws @xowap @CurtAirborne')

        self.assertEqual(t0.users[0].get('user'), '@nano')
        self.assertEqual(t0.users[1].get('user_formated'), 'pastaws')
        self.assertEqual(t0.users[2].get('url'), 'https://twitter.com/xowap')
        self.assertEqual(t0.users[3].get('user'), '@CurtAirborne')

    def test_hashtags(self):
        t0 = Pytter('this is an #hashtag post to test #Pytter')

        self.assertEqual(t0.hashtags[0].get('text'), 'hashtag')
        self.assertEqual(t0.hashtags[1].get('hashtag'), '#Pytter')

    def test_getters(self):
        text = 'this super tweet talk about #twitter @superplanet @frog http://duckduckgo.com'
        t = Pytter(text)

        self.assertEqual(t.get_text(), text)
        self.assertEqual(t.get_hashtags()[0].get('text'), 'twitter')
        self.assertEqual(t.get_urls()[0].get('url'), 'http://duckduckgo.com')
        self.assertEqual(t.get_users()[0].get('user'), '@superplanet')


if __name__ == '__main__':
    unittest.main()
