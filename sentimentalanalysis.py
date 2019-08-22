import glob
import os
import pandas as pd
#sentimental analysis on dataset with comments, timeseries analysis on timestamp
csvfile1 = 'CommentsJan2018.csv'
fields1=['articleID','userID','createDate','newDesk','sectionName','commentBody','userLocation']
csvfile2 = 'ArticlesJan2018.csv'
fields2=['articleID','pubDate','typeOfMaterial','headline','keywords']

# print out to a new csv file
df1 = pd.read_csv(csvfile1,usecols=fields1, dtype={'createDate': str})
df2 = pd.read_csv(csvfile2,usecols=fields2)
df3=pd.merge(df1, df2, on='articleID', how='inner')

#******************* timeseries in simple way ******************************
#converting string timestamps or datetime into datetime format
df3[ 'pubDate'] =  pd.to_datetime(df3 ['pubDate']).astype('datetime64[ns]') 

#creationdate is the date of user rating
#pubDate is date of publication date of article
from datetime import datetime
df3['creationdate'] = df3['createDate'].map(lambda d: datetime.utcfromtimestamp(int(d)))
df3 = df3.set_index('creationdate')

creating time series data into granular details of time
# Add columns with year, month, weekday, hour, minute, second name
#https://pandas.pydata.org/pandas-docs/version/0.24.2/reference/api/pandas.DatetimeIndex.html
df3['Year'] = df3.index.year
df3['Month'] = df3.index.month
df3['Weekday Name'] = df3.index.weekday_name
df3['Hour'] = df3.index.hour
df3['Minute'] = df3.index.minute
df3['Second'] = df3.index.second
df3['Time'] = df3.index.time

# Display a random sampling of 5 rows
df3.sample(5, random_state=0)

#***************** Sentimental anlysis to convert comment into rating ************************
#actual sentimental anlysis give us conversion into score [-1 to 1] and into positive, neutral or negative but we need 1-5 ratings for our model

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
   # Create a SentimentIntensityAnalyzer object. 
sid_obj = SentimentIntensityAnalyzer() 
def sentiment_scores(sentence): 
  
  
    # polarity_scores method of SentimentIntensityAnalyzer 
    # oject gives a sentiment dictionary. 
    # which contains pos, neg, neu, and compound scores. 
    sentiment_dict = sid_obj.polarity_scores(sentence) 
    overall=sentiment_dict['compound']
    overall_sentiment=' '
  
    # decide sentiment as positive, negative and neutral 
    if overall >= 0.05 : 
       overall_sentiment="Positive" 
  
    elif overall <= - 0.05 : 
        overall_sentiment="Negative"
  
    else : 
        overall_sentiment="Neutral" 
   
    return  overall_sentiment
  
  def sentiment_scores_detailed(sentence): 
  
   
    # polarity_scores method of SentimentIntensityAnalyzer 
    # oject gives a sentiment dictionary. 
    # which contains pos, neg, neu, and compound scores. 
    sentiment_dict = sid_obj.polarity_scores(sentence) 
    overall=sentiment_dict['compound']*100
    overall_sentiment=' '
  
    # decide sentiment as positive, negative and neutral 
    if overall >= 55 and overall <=100 : 
       overall_sentiment="5" 
  
    elif overall >=5 and overall < 55 : 
        overall_sentiment="4"
  
    elif overall > -5 and overall < 5 : 
        overall_sentiment="3"
   
    elif overall > -50 and overall <= -5 : 
        overall_sentiment="2"
    elif overall <= -50 : 
        overall_sentiment="1" 
   
    return  overall_sentiment
  
 df3['overall_sentiment'] =df3['commentBody'].apply(lambda Text: sentiment_scores(Text))
df3['rating'] =df3['commentBody'].apply(lambda Text: sentiment_scores_detailed(Text))
df3.to_csv("sentimented")
        
        
