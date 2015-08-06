# Pytter

### A simple Python module to parse your plain text tweets

```python
>>> from pytter.pytter import Pytter

>>> # your tweet in plain text
>>> text = 'This is my super last #tweet ! @pastaws @twitter ! let\'s visit : http://duckduckgo.com !'

>>> # call Pytter
>>> t = Pytter(text)

>>> # now, you can access to all tha datas your tweet contains
>>> # Let's get a quick tour

>>> t.get_text()
"This is my super last #tweet ! @pastaws @twitter ! let\'s visit : http://duckduckgo.com !"

>>> # get_users(), get_hashtags() and get_urls() will return
>>> # a list of dictionary
>>> t.get_users()
[
	{
	   'url': 'https://twitter.com/pastaws',
	   'user_formated': 'pastaws',
	   'html': '<a href="https://twitter.com/pastaws" target="_blank" class="tweet_user">@pastaws</a>',
	   'user': '@pastaws',
   }, 
   {
	   'url': 'https://twitter.com/twitter',
	   'user_formated': 'twitter',
	   'html': '<a href="https://twitter.com/twitter" target="_blank" class="tweet_user">@twitter</a>',
	   'user': '@twitter',
	}
]

>>> t.get_urls()
[
	{
		'url': 'http://duckduckgo.com', 
		'html': '<a href="http://duckduckgo.com" target="_blank" class="tweet_url">http://duckduckgo.com</a>',
	}
]

>>> t.get_hashtags()
[
	{
	'html': '<a href="https://twitter.com/hashtag/tweet" target="_blank" class="tweet_hashtag">#tweet</a>', 
	'url': 'https://twitter.com/hashtag/tweet', 
	'text': 'tweet',
	'hashtag': '#tweet'
	}
]

>>> #get_html() return the tweet formated with all html tags
>>> t.get_html()
'This is my super last <a href="https://twitter.com/hashtag/tweet" target="_blank" class="tweet_hashtag">#tweet</a> ! <a href="https://twitter.com/pastaws" target="_blank" class="tweet_user">@pastaws</a> <a href="https://twitter.com/twitter" target="_blank" class="tweet_user">@twitter</a> ! let\'s visit : <a href="http://duckduckgo.com" target="_blank" class="tweet_url">http://duckduckgo.com</a> !'
```

#### You can also set the html/css classes you want to give for each kind of anchor tags

There is two way to do it.

```python
>>> from pytter.pytter import Pytter

>>> # Directly on Pytter call
>>> custom_classes = {
    'user': 'my_user_anchor_class',
    'url': 'my_url_class',
    'hashtag': 'my_hashtag_class'
}

>>> text = 'this is a #tweet from @myusername, visit me at http://website.com'
>>> t = Pytter(text, custom_classes)

>>> # now if you check your html links
>>> t.get_hashtags()[0].get('html')
'<a href="https://twitter.com/hashtag/tweet" target="_blank" class="my_hashtag_class">#tweet</a>'

>>> # You can also set custom class next your Pytter call
>>> t = Pytter(text)
>>> t.set_html_class(custom_classes)
>>> t.parse()
>>> t.get_html_classes()
{'hashtag': 'my_hashtag_class', 'url': 'my_url_class', 'user': 'my_user_anchor_class'}
```

#### You can get all of this stuff in one big dictionary or JSON
```python
>>> # t.get_json() will give you the same result in JSON
>>> t.get_all()
{
	'hashtags': [
        {
            'html': '<a href="https://twitter.com/hashtag/tweet" target="_blank" class="my_hashtag_class">#tweet</a>',
            'url': 'https://twitter.com/hashtag/tweet',
            'text': 'tweet',
            'hashtag': '#tweet',
        }
    ],
    'urls': [
        {
            'url': 'http://website.com',
            'html': '<a href="http://website.com" target="_blank" class="my_url_class">http://website.com</a>'
        }
    ],
    'formated': 'this is a <a href="https://twitter.com/hashtag/tweet" target="_blank" class="my_hashtag_class">#tweet</a> from <a href="https://twitter.com/myusername" target="_blank" class="my_user_anchor_class">@myusername</a>, visit me at <a href="http://website.com" target="_blank" class="my_url_class">http://website.com</a>',
    'text': 'this is a #tweet from @myusername, visit me at http://website.com',
    'users': [
        {
            'url': 'https://twitter.com/myusername',
            'user_formated': 'myusername',
            'html': '<a href="https://twitter.com/myusername" target="_blank" class="my_user_anchor_class">@myusername</a>',
            'user': '@myusername',
        }
    ],
    'tweet_length': 65,
    'html_classes': {
        'hashtag': 'my_hashtag_class',
        'url': 'my_url_class',
        'user': 'my_user_anchor_class'
    },
}

```
