## Introduce
a tiny script for operating Craigslist.org with out any bloated frame such as selenium/scrapy.

just `requests` and `re` .


## Usage Example
```
# create a instance of Craigslist function
account1 = Craigslist(craigslist_cookies)

# create a new post in Craigslist.org and get the path for POST method
post_path = account1.creat_post()

# set first 3 pages paramaters
account1.set_params(post_path, 'subarea')
account1.set_params(post_path, 'type')
account1.set_params(post_path, 'hcat')
```
