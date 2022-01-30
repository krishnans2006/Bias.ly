# Bias.ly

## Inspiration
As high school students, we're constantly told to never believe everything we see on the internet. Unfortunately, the same people who offered this wise advice sometimes fail to hail it. Understanding the nuances in biases from several different news websites (Fox News + CNN), we found a need to offer clarity behind the biases of different popular news sources. Hopefully, by bringing such a tool to the hands of others, we can all be a little more weary of the different narratives being pedaled along.

## What it does
Bias.ly is a tool to discover biases in different news sources. Initially scraping news websites for initial data based on a keyword, we load data such as headlines, description, and content into a dictionary, then depositing them into a list. After conversions to JSON and Pandas DataFrames, we then begin cleaning the data to prepare it for sentiment analysis to discover biases. Specifically, utilizing tokenization and lammetization, we begin our sentiment analysis for a single news source among the past 14 days of articles. We average the sentiments for each article for each day, and return it to display in a graph on the frontend.

## How we built it

### Backend
The first step in creating the back end structure of our project was implemneting the news api to the project in order to have a good list of article names which we could draw the analysis from. The step first invovled requesting articles that fell under a certain keyword and date. We then had to take the object, which was returned, and prepare it for the sentiment analysis portion of the code by removing any non ASCII characters, expanding common abreviations such as weren't or haven't, removed stop words, and toxenized the data string. Following this step we began the sentiment calculcation by using the NLTK api to obtain the string datas polarity of either a negative or positive sentiment value.Finsihing up the backend, we optimized the algoritihm used to obtain articles in order to send significantly less requests and ordered them in a manner that would be best for the front end when compiling the data into graph form. In addition we split more of the program into functions, helping us isolate any bugs we had as well as allowing for the front end to easily call the "get_data" function to input wanted websites and the key word, returning a list which includes the 2 day average, over a 14 day span, of the search term's sentiment and the number of articles about that keyword searched for the 2 days.  

Credit to [Farooq](https://github.com/farooq96/News-Sentiment-Analysis-in-Python) for his code for sentiment analysis of news websites; we wouldn't have been able to do it without his documentation.

### Frontend

The frontend involved creating multiple webpages designed with HTML, styled with CSS, and implemented with JavaScript. These webpages were served using our backend, letting us add dynamic content to them for displaying data. The Bootstrap framework was used for styling and responsiveness.A

The frontend involves three pages: A search page, a loading page, and the results page. The search page lets you search for a word and filter it by news source. Once the user submits a request to search for a word and news network, the loading page appears while the server analyzes the news articles. Once done, two fancy graphs are displayed using [Chart.js](https://www.chartjs.org/) displaying the total article count and determined sentiment values.


## Challenges we ran into
The first challenge that we came across was to find the best sentiment API for our speicific use case that is relatively simple to use and easy. We first looked at Google's, Natural Language, API, but was not the best for use in our project, so we turned to NLTK.

A challenge that we came across as we developed the backend was of how to effectively implement the news API without using an excess amount of requests. We solved this by requesting the API through different days instead of per domain, which decreased our total requests needed by around 900%.

FRONT END TEAM INSERT YOUR STUFF HERE
The front end team also ran into issues while creating the website. The "See How It Works" button was really difficult to code
There were, of course, a few challenges that were just results of careless oversights of the API documentation and what not.



## Accomplishments that we're proud of
As highschoolers interested in Computer Science, building a fullstack application successfully and in less than 12 hours that incorporates techniques such as natural language processing and web-scraping is something we're extremely proud of. Amatuers in writing code, we're proud of being able to persevere through the unknown waters of sentiment analysis. Lastly, we're most proud of creating a brilliant web-app that offers true value to those who use it; our mission has always been to bring a positive impact to the world through code, and this project embodies that very idea.

## What we learned
We learned a great deal in a varitey of subjects. First and foremost, as our first hackathon (3 of 4 members) we gained valuable experience developing a sophisticated yet useful app in a short amount of time. Beyond just learning how hackathons work, we dove deeper into the idea that inspired the project: the scope of bias and narratives are much beyond what we may initially believe and they hold a stronger grasp on people's beliefs than we currently think - our learnings, after diving deep into this subject, have reinforced our belief of the importance of bias checkers and ways to ensure our sources of information are objective. In addition, we learned the basics of sentiment analysis and natural language processing: tokenization, lammetization, and removing parts of sentences like stop words, punctuation, and neutral words.

## What's next for Bias.ly
As for Bias.ly, we're looking to get it hosted on a website to share our tool with as many people as possible. We hope that our small web-app will continue to bring value to anyone who uses it, and ultimately grows to encompass more websites, greater complexity in search terms, and more comprehensive analytics. As we write this, we've already begun working on implementing topic modeling and more diverse attitudes to our tool: we hope that it slowly becomes a more useful and important idea that many people consider before taking information for granted. Objectivity is crucial, but subjectivity is commonplace.
