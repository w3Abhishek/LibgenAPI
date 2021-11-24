import requests
from bs4 import BeautifulSoup
import random

from requests.api import head
# http://libgen.st/search.php?req=Python&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def

libraryDomain = 'http://libgen.st'
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}

def search(query):
    bookDetails = {}
    url = libraryDomain + '/search.php?req=' + query + '&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('tr', attrs={"valign":True, "bgcolor": True})
    try:
        for count, result in enumerate(results):
            if count != 0:
                bookDetail = result.find_all('td')
                bookAuthor = bookDetail[1].find('a')
                # bookISBN = str(bookDetail[2].find('a'))
                bookTitle = bookDetail[2].find('a')
                bookPublisher = bookDetail[3].text
                bookID = bookDetail[0].text
                bookAuthorName = bookAuthor.text
                bookAuthorURL = bookAuthor['href']
                # bookISBN = bookISBN.split('<i>')[2].split('</i>')[0]
                # print(bookISBN)
                bookYear = bookDetail[4].text
                bookPages = bookDetail[5].text
                bookLanguage = bookDetail[6].text
                bookSize = bookDetail[7].text
                bookExtension = bookDetail[8].text
                md5 = bookTitle['href'].split('=')[1]
                bookDetails[count] = {
                    'bookID': bookID,
                    'bookTitle': bookTitle.text,
                    'author': bookAuthorName,
                    'authorLink': bookAuthorURL,
                    # 'bookISBN':bookISBN,
                    'publisher': bookPublisher,
                    'year': bookYear,
                    'pages': bookPages,
                    'lang':bookLanguage,
                    'size': bookSize,
                    'fileFormat':bookExtension,
                    'md5':md5
                    }
            else:
                pass
            count += 1
        return bookDetails
    except:
        bookDetails = {}
        return bookDetails

def getBook(query):
    md5 = query
    url = 'http://library.lol/main/' + md5
    r = requests.get(url, headers=headers)
    nisoup = BeautifulSoup(r.text, 'html.parser')
    allLinks = nisoup.find_all('a')
    mainLink = allLinks[0]['href']
    try:
        coverLink = nisoup.find('img')['src']
    except:
        coverLink = ''
    result = {'cover':coverLink, filelink':mainLink, 'altLinks':[allLinks[1]['href'], allLinks[2]['href'], allLinks[3]['href'], allLinks[4]['href']]}
    return result
