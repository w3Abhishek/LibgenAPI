from bs4 import BeautifulSoup
import requests
import random
import html
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}
proxyDomain = 'http://libgen.st/'
downDomain = "http://library.lol/main/"
def search(query):
  queryURL = '%ssearch.php?req=%s&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def'%(proxyDomain,query)
  response = requests.get(queryURL,headers=headers)
  headDoc = BeautifulSoup(response.text, 'html.parser')
  result = headDoc.find_all("a", attrs={"id":True, "title":True, "href":True})
  count = 0
  searchres = "Results: \n\n"
  apiResponse = {}
  for i in result:
    pageLink = downDomain + i['href'].split('md5=')[1]
    srequest = requests.get(pageLink, headers = headers)
    srequest.encoding = 'utf-8'
    nisoup = BeautifulSoup(srequest.text, 'html.parser')
    bookDetails = nisoup.find_all("p")
    pageres = str(nisoup.h2)
    bookName = nisoup.h1.text
    fileLink = pageres.split('"')[1]
    bookcover = "http://library.lol/" + str(nisoup.img['src'])
    altL = nisoup.find_all("a")
    try:
      authorName = bookDetails[0].text.replace('Author(s): ', '')
    except:
      authorName = "Anonymous"
    apiResponse[count] = {}
    altLinks = []
    for i in range(1, 5):
      altLinks[i-1] = altL[i]['href']
    apiResponse[count]['altlinks'] = altLinks
    apiResponse[count]['bookname'] = str(bookName)
    apiResponse[count]['filelink'] = str(fileLink)
    apiResponse[count]['authorname'] = str(authorName)
    apiResponse[count]['cover'] = str(bookcover[0]['src'])
    count += 1
  apiResponse = {'count':count, 'results':apiResponse}
  return apiResponse
