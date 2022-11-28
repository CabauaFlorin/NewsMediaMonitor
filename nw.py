import requests
from newsapi import NewsApiClient

q = input()
newsapi = NewsApiClient(api_key = "ba79436deb7540b195686c7e9e046a72")
data = newsapi.get_everything(q, page=1, page_size=100) #se mai poate adauga language='en' sau/si from_param='2019-06-15'
results = data['articles'].copy()
for i in range(10):
    print(i+1, ".", results[i]['title'], "->", results[i]['source']['name'])

# def getNews():
#     api = "ba79436deb7540b195686c7e9e046a72"
#     url = "https://newsapi.org/v2/top-headlines?country=ro&apiKey=" + api
#     news = requests.get(url).json()

#     articles = news["articles"]
#     my_articles = []
#     my_news = ""

#     for article in articles:
#         my_articles.append(article["title"])

#     for i in range(10):
#         my_news = my_news + my_articles[i] + "\n"

#     print(my_news)

# url = f"https://newsapi.org/v2/top-headlines?country=ro&apiKey={api}"

# response = requests.get(url)

# data = response.json()
# articles = data.get('articles')

# for title in articles:
#     print(title['source'])