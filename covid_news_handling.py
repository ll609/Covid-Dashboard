import requests
import sched, time
from config_handler import config_handler
import logging

def news_API_request(covid_terms: str="Covid COVID-19 coronavirus") -> list[dict]:
    terms = covid_terms.split()
    logging.info(f'Covid search terms split apart: {terms}')
    news = requests.get(f'https://newsapi.org/v2/everything?q={terms[0]} OR {terms[1]} OR {terms[2]} \
    &language=en&pageSize=5&apiKey={config_handler()[0]}')
    logging.debug('News API retrieved')
    results = news.json()
    logging.debug('News API data read into a dictionary using JSON')
    '''Searches for news articles which include any of the covid_terms specified above. The articles
    will only be in English and a maximum of 5 will be returned in order not to put too much on the
    webpage. The results are read by JSON as a dictionary, with a title and content matching to each
    article'''
    articles = results['articles']
    logging.info('Articles extracted from news API data')
    headlines_matching = []
    for ar in articles:
        title = ar['title']
        content = ar['content']
        article = {"title": title, "content": content}
        headlines_matching.append(article)
    logging.info('Title and contents of each article added to list')
    '''Appends each of the corresponding articles into a list. Each article is stored as a dictionary,
    with a title and content'''   
    return headlines_matching

def update_news(update_interval: int, update_name: str):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(update_interval, 1, news_API_request)
    logging.debug('News update data scheduler set')
    '''Runs the scheduler, which calls the news_API_request function once the time in the update_interval
    variable is reached'''
    s.run(blocking=False)
    logging.debug('News update data scheduler running')
    #Runs the scheduler without holding up other operations in the program