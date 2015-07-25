# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# pytter
# copyright (c) 2015 Vincent Loy
# Vincent Loy <vincent.loy1@gmail.com>
import re
import json

HTML_CLASSES = {
    'user': 'tweet_user',
    'url': 'tweet_url',
    'hashtag': 'tweet_hashtag'
}


class Pytter:
    def __init__(self, tweet, html_class=None):
        self.text = tweet
        self.formated_tweet = tweet
        self.length = len(tweet)
        self.urls = []
        self.users = []
        self.hashtags = []

        # contain all informations about the tweet
        self.tweet = None
        self.tweet_json = None

        if (html_class is None) or (type(html_class) is not dict):
            self.html_class = HTML_CLASSES
        else:
            self.html_class = html_class

        self.parse()

    def set_html_class(self, html_class):
        """
        Set html_class
        :param html_class: dict
        """
        if html_class.get('user') and html_class.get('url') and html_class.get('hashtag'):

            if (type(html_class.get('user')) is str) and \
                            type(html_class.get('url')) is str and \
                            type(html_class.get('hashtag')) is str:
                self.html_class = html_class

            else:
                raise ValueError('html_class must contain strings')

        else:
            required_keys = ', '.join(['user', 'url', 'hashtag'])
            raise ValueError('Error setting html_class, the dictionnary have required keys : {keys}'
                             .format(keys=required_keys))

    def parse_url(self):
        url_regex = '(^|\s)((f|ht)tps?://([^ \t\r\n]*[^ \t\r\n\)*_,\.]))'
        match = re.findall(url_regex, self.text)

        if match:
            for m in match:
                link = '<a href="{url}" target="_blank" class="{tweetclass}">{text}</a>' \
                    .format(url=m[1], text=m[1], tweetclass=self.html_class['url'])

                d = {
                    'url': m[1],
                    'text': m[1],
                    'html': link
                }

                self.urls.append(d)
                self.formated_tweet = self.formated_tweet.replace(m[1], link)

    def parse_users(self):
        user_regex = '(\B@([a-zA-Z0-9_]+))'
        match = re.findall(user_regex, self.text)

        if match:
            for m in match:
                base_url = 'https://twitter.com/'
                link = '<a href="{base_url}{user_only}" target="_blank" class="{tweetclass}">{text}</a>' \
                    .format(base_url=base_url, user_only=m[1], text=m[0], tweetclass=self.html_class['user'])

                d = {
                    'user': m[0],
                    'user_formated': m[1],
                    'url': base_url + m[1],
                    'html': link
                }

                self.formated_tweet = self.formated_tweet.replace(m[0], link)
                self.users.append(d)

    def parse_hashtags(self):
        hashtag_regex = '(\B#([á-úÁ-Úä-üÄ-Üa-zA-Z0-9_]+))'
        match = re.findall(hashtag_regex, self.text)

        if match:
            for m in match:
                base_url = 'https://twitter.com/hashtag/'
                link = '<a href="{base_url}{hashtag_text}" target="_blank" class="{tweetclass}">{hashtag}</a>' \
                    .format(base_url=base_url, hashtag_text=m[1], hashtag=m[0], tweetclass=self.html_class['hashtag'])

                d = {
                    'text': m[1],
                    'hashtag': m[0],
                    'url': base_url + m[1],
                    'html': link
                }

                self.formated_tweet = self.formated_tweet.replace(m[0], link)
                self.hashtags.append(d)

    def parse(self):
        self.parse_hashtags()
        self.parse_users()
        self.parse_url()

        self.tweet = {
            'users': self.users,
            'urls': self.urls,
            'hashtags': self.hashtags,
            'text': self.text,
            'tweet_length': self.length,
            'formated': self.formated_tweet,
            'html_classes': self.html_class
        }

        self.tweet_json = json.dumps(self.tweet)
