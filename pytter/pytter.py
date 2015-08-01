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

USER_REGEX = '(\B@([a-zA-Z0-9_]+))'
URL_REGEX = '(^|\s)((f|ht)tps?://([^ \t\r\n]*[^ \t\r\n\)*_,\.]))'
HASHTAG_REGEX = '(\B#([á-úÁ-Úä-üÄ-Üa-zA-Z0-9_]+))'


class Pytter:
    def __init__(self, tweet, html_class=None):
        self.text = tweet
        self.formated_tweet = None
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

    """
    PARSERS
    """

    def parse_url(self):
        match = re.findall(URL_REGEX, self.text)

        if match:
            for m in match:
                link = '<a href="{url}" target="_blank" class="{tweetclass}">{text}</a>' \
                    .format(url=m[1], text=m[1], tweetclass=self.html_class['url'])

                self.urls.append({
                    'url': m[1],
                    'html': link
                })
                self.formated_tweet = self.formated_tweet.replace(m[1], link)

    def parse_users(self):
        match = re.findall(USER_REGEX, self.text)

        if match:
            for m in match:
                base_url = 'https://twitter.com/'
                link = '<a href="{base_url}{user_only}" target="_blank" class="{tweetclass}">{text}</a>' \
                    .format(base_url=base_url, user_only=m[1], text=m[0], tweetclass=self.html_class['user'])

                self.formated_tweet = self.formated_tweet.replace(m[0], link)
                self.users.append({
                    'user': m[0],
                    'user_formated': m[1],
                    'url': base_url + m[1],
                    'html': link
                })

    def parse_hashtags(self):
        match = re.findall(HASHTAG_REGEX, self.text)

        if match:
            for m in match:
                base_url = 'https://twitter.com/hashtag/'
                link = '<a href="{base_url}{hashtag_text}" target="_blank" class="{tweetclass}">{hashtag}</a>' \
                    .format(base_url=base_url, hashtag_text=m[1], hashtag=m[0], tweetclass=self.html_class['hashtag'])

                self.formated_tweet = self.formated_tweet.replace(m[0], link)
                self.hashtags.append({
                    'text': m[1],
                    'hashtag': m[0],
                    'url': base_url + m[1],
                    'html': link
                })

    """
    GETTERS
    """
    def get_all(self):
        return self.tweet

    def get_json(self):
        return self.tweet_json

    def get_hashtags(self):
        return self.hashtags

    def get_users(self):
        return self.users

    def get_urls(self):
        return self.urls

    def get_html(self):
        return self.formated_tweet

    def get_text(self):
        return self.text

    def get_html_classes(self):
        return self.html_class

    """
    THE PARSE FUNCTION
    """

    def parse(self):
        self.formated_tweet = self.text
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
