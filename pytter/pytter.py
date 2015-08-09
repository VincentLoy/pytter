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
        if (html_class is None) or (type(html_class) is not dict):
            self.html_class = HTML_CLASSES
        else:
            self.html_class = self.set_html_class(html_class)

        self.text = tweet
        self.formated_tweet = None
        self.length = len(tweet)
        self.formated_tweet = self.text
        self.urls = list(self.parse_url())
        self.users = list(self.parse_users())
        self.hashtags = list(self.parse_hashtags())

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

    def set_html_class(self, html_class):
        """
        Set html_class
        :param html_class: dict
        """
        if ('user' in html_class) and ('url' in html_class) and ('hashtag' in html_class):

            for k, v in html_class.items():
                if type(v) is not str:
                    raise ValueError('Only string values allowed for html_class, {} is {}'.format(v, type(v)))

            return html_class

        else:
            required_keys = ', '.join(['user', 'url', 'hashtag'])
            raise ValueError('Error setting html_class, the dictionnary have required keys : {keys}'
                             .format(keys=required_keys))

    # ---
    # PARSERS
    # ---
    def parse_url(self):
        match = re.findall(URL_REGEX, self.text)

        if match:
            for m in match:
                link = '<a href="{url}" target="_blank" class="{tweetclass}">{text}</a>' \
                    .format(url=m[1], text=m[1], tweetclass=self.html_class['url'])

                self.formated_tweet = self.formated_tweet.replace(m[1], link)
                yield {
                    'url': m[1],
                    'html': link
                }

    def parse_users(self):
        match = re.findall(USER_REGEX, self.text)

        if match:
            for m in match:
                base_url = 'https://twitter.com/'
                link = '<a href="{base_url}{user_only}" target="_blank" class="{tweetclass}">{text}</a>' \
                    .format(base_url=base_url, user_only=m[1], text=m[0], tweetclass=self.html_class['user'])

                self.formated_tweet = self.formated_tweet.replace(m[0], link)
                yield {
                    'user': m[0],
                    'user_formated': m[1],
                    'url': base_url + m[1],
                    'html': link
                }

    def parse_hashtags(self):
        match = re.findall(HASHTAG_REGEX, self.text)

        if match:
            for m in match:
                base_url = 'https://twitter.com/hashtag/'
                link = '<a href="{base_url}{hashtag_text}" target="_blank" class="{tweetclass}">{hashtag}</a>' \
                    .format(base_url=base_url, hashtag_text=m[1], hashtag=m[0], tweetclass=self.html_class['hashtag'])

                self.formated_tweet = self.formated_tweet.replace(m[0], link)
                yield {
                    'text': m[1],
                    'hashtag': m[0],
                    'url': base_url + m[1],
                    'html': link
                }

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
