## Project Information
#### Team Members: Simrun Mutha & Melody Chiu

The goal of this CoffeeFinder project is to find what makes each coffee brand unique in terms of flavor. In order to do this, our project involves four major portions of code:

1. Data Collection
    This involves scraping all the reviews for an Amazon product through its All Reviews page. The code for this portion can be found in scraping_reviews.py

2. Data Processing
    This involves processing the data scraped from the Amazon site. The reviews are sorted through to find adjectives that relate to coffee flavor profiles. The code for this portion can be found in processing_data.py

3. Data Visualization
    This involves illustrating the words output from processing and their frequency. The code for this portion can be found in visualizing_data.py

4. Loading
    This involves loading the information about the coffee brands and frequent nouns in Amazon reviews that are unrelated to coffee flavor. The code for this portion can be found in loading.py

## Installing Libraries

For the project we used various libraries in order to carry out various tasks within our project. Two of these libraries are nltk and WordCloud. To install nltk, files were downloaded from this link: http://pypi.python.org/pypi/nltk and then the command import nltk was carried out at the top of the python file. To install WordCloud, the command pip install “pip install wordcloud” has to be carried out in the bash terminal and then the line from wordcloud import WordCloud, STOPWORDS has to be run at the top of any python file. 
