import urllib.request
import urllib.parse

url = 'https://baconipsum.com/api/?type=meat-and-filler'                # куда
values = {'key': 'value'}                                               # dict
data = urllib.parse.urlencode(values)                                   # кодирование
# data = json.dumps(values)                                             # json
data = data.encode('utf-8')                                             # bytes
req_post = urllib.request.Request(url, data)                            # объект POST
the_page = urllib.request.urlopen(req_post)                             # отправил
the_page = the_page.read().decode()                                     # читаю ответ

print(the_page)
