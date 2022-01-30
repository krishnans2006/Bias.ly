import requests
import json
import numpy as np
import pandas as pd
import nltk 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import re
import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake 
from datetime import date
import time
from dotenv import load_dotenv
from os import getenv

load_dotenv()

url = 'https://newsapi.org/v2/everything?'

news_api_key = os.getenv("APIKEY")
print(news_api_key)


# THE API KEY TO USE BEFORE SUBMITTING = ''
# old api key: 78cef6f2c89145ff986c92327743290f

pageSize = 100
startTime = time.time()


# function to take raw data from the API and process it into a list inorder to trnasform it into a pandas dataframe
def get_articles(file): 

    article_results = [] 
    
    for i in range(len(file)):
        article_dict = {}
        article_dict['title'] = file[i]['title']
        article_dict['source'] = file[i]['source']
        article_dict['description'] = file[i]['description']
        article_dict['content'] = file[i]['content']
        article_dict['pub_date'] = file[i]['publishedAt']
        # article_dict['url'] = file[i]["url"]
        article_results.append(article_dict)

    return article_results


# R.I.P dayCalc [date.today() - time.time()]
# def dayCalc(dayNum):
#     currentDay = date.today()
#     if currentDay - 14 & 2 == 0:
#         currentDay =  (currentDay) - (14 - (dayNum + 2))
#     else:
#         currentDay (currentDay - 1) - (14 - (dayNum + 2))
    

# Collecting the first 100 articles about ireland to check the API and the working of the function 
def search_return_df(word, website, startDate, endDate):
    news_articles_df = pd.DataFrame()
    # domains = ['wsj.com','aljazeera.com','bbc.co.uk', 'nytimes.com','bloomberg.com',
    #             'cnn.com','foxnews.com','reuters.com','washingtonpost.com']
    
    # domains = ['wsj.com','aljazeera.com','bbc.co.uk', 'nytimes.com']
    # for domain in domains:
    parameters_headlines = {
    'q': word,
    'domains': website,
    'sortBy':'popularity',
    'pageSize': pageSize,
    'apiKey': news_api_key,
    'language': 'en',
    'from' : '2022-01-{x}'.format(x = startDate),
    'to': '2022-01-{e}'.format(e = endDate)
    }
    rr = requests.get(url, params = parameters_headlines)
    data = rr.json()
    try:
        responses = data["articles"]
    except KeyError:
        print(data)
        return False

    # news_articles_df = pd.DataFrame(get_articles(responses))
    news_articles_df=news_articles_df.append(pd.DataFrame(get_articles(responses)))


    # droping the rows with missing data 
    news_articles_df.dropna(inplace=True)
    news_articles_df = news_articles_df[~news_articles_df['description'].isnull()]

    news_articles_df['combined_text'] = news_articles_df['title'].map(str) +" "+ news_articles_df['content'].map(str)
    return news_articles_df

# Function to remove non-ascii characters from the text
def _removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)
# function to remove the punctuations, apostrophe, special characters using regular expressions
def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = text.replace('(ap)', '')
    text = re.sub(r"\'s", " is ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"\\", "", text)
    text = re.sub(r"\'", "", text)    
    text = re.sub(r"\"", "", text)
    text = re.sub('[^a-zA-Z ?!]+', '', text)
    text = _removeNonAscii(text)
    text = text.strip()
    return text
# stop words are the words that convery little to no information about the actual content like the words:the, of, for etc
def remove_stopwords(word_tokens):
    filtered_sentence = [] 
    stop_words = stopwords.words('english')
    specific_words_list = ['char', 'u', 'hindustan', 'doj', 'washington'] 
    stop_words.extend(specific_words_list )
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    return filtered_sentence
# function for lemmatization 
def lemmatize(x):
    lemmatizer = WordNetLemmatizer()
    return' '.join([lemmatizer.lemmatize(word) for word in x])

# splitting a string, text into a list of tokens
tokenizer = RegexpTokenizer(r'\w+')
def tokenize(x): 
    return tokenizer.tokenize(x)

def polarityCalculator(newsDF):
    newsDF['combined_text'] = newsDF['combined_text'].map(clean_text)
    newsDF['tokens'] = newsDF['combined_text'].map(tokenize)
    newsDF['tokens'] = newsDF['tokens'].map(remove_stopwords)
    newsDF['lems'] =newsDF['tokens'].map(lemmatize)

    # finding the keywords using the rake algorithm from NLTK
    # rake is Rapid Automatic Keyword Extraction algorithm, and is used for domain independent keyword extraction
    newsDF['keywords'] = ""
    for index,row in newsDF.iterrows():
        comb_text = row['combined_text']
        r = Rake()
        r.extract_keywords_from_text(comb_text)
        key_words_dict = r.get_word_degrees()
        row['keywords'] = list(key_words_dict.keys())

    # applying the fucntion to the dataframe
    newsDF['keywords'] = newsDF['keywords'].map(remove_stopwords)
    newsDF['lems'] =newsDF['keywords'].map(lemmatize)

    # calculating the polarity of the news articles 
    from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
    sia = SIA()
    results = []
    for line in newsDF['lems'] :
        pol_score = sia.polarity_scores(line)
        pol_score['headline'] = line
        results.append(pol_score)

    # Creating a new dataframe of only the polarity score, the headline and the source of the news 
    headlines_polarity = pd.DataFrame.from_records(results)
    temp = []
    for line in newsDF['source'] :
        temp.append(line)
    headlines_polarity['source'] =temp
    
    temp = []

    for line in newsDF['pub_date']:
        temp.append(line)
    headlines_polarity['pub_date'] =temp

    # categorize news as positive or negative based on the compound score obtained
    headlines_polarity['label'] = 0
    # I have considered the news as positive if the compound score is greater than 0.2 hence the label 1
    headlines_polarity.loc[headlines_polarity['compound'] > 0.2, 'label'] = 1
    # if the compound score is below 0.2 then it is considered negative 
    headlines_polarity.loc[headlines_polarity['compound'] < -0.2, 'label'] = -1
    # word count of news headlines is calculated
    headlines_polarity['word_count'] = headlines_polarity['headline'].apply(lambda x: len(str(x).split()))

    return headlines_polarity['compound']



def get_data(wordSearch, website):
    if website == "all":
        website = 'wsj.com, aljazeera.com, bbc.co.uk , nytimes.com, bloomberg.com, cnn.com, foxnews.com, reuters.com ,washingtonpost.com'
    compoundAvg = []
    articlesPerDay = []
    startDate = 15
    endDate = 17
    ooga = search_return_df(wordSearch, website, startDate, endDate)
    print(ooga)
    try:
        ooga.empty
    except:
        return False

    for i in range(7):
        ooga = search_return_df(wordSearch, website, startDate, endDate)
        ooga = polarityCalculator(ooga)
        x = 0
        y = 0
        for v in ooga:
            x += v
            y += 1

        x /= len(ooga)
        compoundAvg.append([x, y])

        # articlesPerDay.append(y)
        # compoundAvg.append(x)

        startDate += 2
        endDate += 2

    return compoundAvg #and articlesPerDay

if __name__ == "__main__":
    get_data("biden", 'wsj.com, foxnew.com') # If you want to use multiple websites type like, "foxnews.com, cnn.com"
# domains = ['wsj.com','aljazeera.com','bbc.co.uk', 'nytimes.com','bloomberg.com',
    #             'cnn.com','foxnews.com','reuters.com','washingtonpost.com']
