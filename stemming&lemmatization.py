# -*- coding: utf-8 -*-
"""Stemming&Lemmatization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XtjES8lTZ7aLU7YNWmC-OHfEFJTZbUdh
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
# %matplotlib inline

from google.colab import files
fifa_ny_la_chic = files.upload()

import io
df = pd.read_csv(io.BytesIO(fifa_ny_la_chic['df.csv']))

mario=mario.iloc[:,1:]
mario.head(2)

path = "/content/novel_final_tweets.csv"

data = pd.read_csv(path)

user_desc_wc.columns=['UsrDesc']
user_desc_wc.head(2)

data.describe()

user_desc_wc.isna().sum()

def remove_spaces(text):
    text=text.strip()
    text=text.split()
    return ' '.join(text)

def edits1(word):
    letters='abcdefghijklmnopqrstuvwxyz'
    splits=[(word[:i], word[i:]) for i in range(len(word)+1)]
    deletes=[L+R[1:] for L,R in splits if R]
    transposes=[L+R[1] +R[0] + R[2:] for L,R in splits if len(R)>1]
    replaces = [L+c+R[1:] for L,R in splits if R for c in letters]
    inserts = [L+c+ R for L,R in splits for c in letters]
    return set(deletes+transposes+replaces+inserts)
def edits2(word):
    return(e2 for e1 in edits1(word) for e2 in edits1(e1))

contraction = {'cause':'because',
              'aint': 'am not',
              'aren\'t': 'are not'}

def mapping_replacer(x,dic):
    for words in dic.keys():
        if ' ' + words + ' ' in x:
            x=x.replace(' '+ words +' ' ,' '+dic[words]+' ' )
    return x

import nltk
nltk.download('punkit')
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer

nltk.LancasterStemmer
ls = LancasterStemmer()
lem = WordNetLemmatizer()
def lexicon_normalization(text):
    words = word_tokenize(text) 
    
    
    # 1- Stemming
    words_stem = [ls.stem(w) for w in words]
    
    # 2- Lemmatization
    words_lem = [lem.lemmatize(w) for w in words_stem]
    return words_lem

pip install emoji

import emoji
import re 
#from emot.emo_unicode import UNICODE_EMO
def convert_emojis(text):
    for emot in emoji.UNICODE_EMOJI:
        text = re.sub(r'('+emot+')', "_".join(emoji.UNICODE_EMOJI[emot].replace(",","").replace(":","").split()), text)
    return text

def clean_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers.'''
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('\'','', text)
    
    return text

from collections import Counter
def remove_stopword(text):
    stop_words = stopwords.words('english')
    stopwords_dict = Counter(stop_words)
    text = ' '.join([word for word in text.split() if word not in stopwords_dict])
    return text

def tokenise(text):
    words = word_tokenize(text) 
    return words

import re
user_desc_wc['UsrDesc'] = user_desc_wc['UsrDesc'].map(lambda x: re.sub(r'\W+', ' ', x))
user_desc_wc['UsrDesc'] = user_desc_wc['UsrDesc'].replace(r'\W+', ' ', regex=True)

user_desc_wc['UsrDesc'] = user_desc_wc['UsrDesc'].apply(lambda x: mapping_replacer(x, contraction))

user_desc_wc['UsrDesc'] = user_desc_wc['UsrDesc'].apply(lambda x: clean_text(x))

from nltk.corpus import stopwords

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

pip install nltk

user_desc_wc['UsrDesc']=user_desc_wc['UsrDesc'].apply(lambda x: remove_stopword(x))

user_desc_wc['UsrDesc']= user_desc_wc['UsrDesc'].apply(lambda x: lexicon_normalization(x))

user_desc_wc.head()

top = Counter([item for sublist in user_desc_wc['UsrDesc'] for item in sublist])
temp = pd.DataFrame(top.most_common(50))
temp.columns = ['Common_words','count']
temp.style.background_gradient(cmap='Blues')

import matplotlib.pyplot as plt
import plotly.express as px

fig = px.bar(temp, x="count", y="Common_words", title='Commmon Words in Selected Text', orientation='h', 
             width=700, height=700,color='Common_words')
fig.show()

from wordcloud import WordCloud, STOPWORDS , ImageColorGenerator

from textblob import TextBlob

def get_tweet_sentiment(tweet): 
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(tweet) 
    
    # set sentiment 
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0: 
        return 'neutral'
    else: 
        return 'negative'

mario['sentiment']=mario['Tweet'].apply(lambda x: get_tweet_sentiment(' '.join(x)))

Positive_sent = mario[mario['sentiment']=='positive']
Negative_sent = mario[mario['sentiment']=='negative']
Neutral_sent = mario[mario['sentiment']=='neutral']

print('Number of tweets with positive sentiment', Positive_sent['sentiment'].count())
print('Number of tweets with negative sentiment', Negative_sent['sentiment'].count())
print('Number of tweets with neutral sentiment', Neutral_sent['sentiment'].count())

#MosT common negative words
top = Counter([item for sublist in Negative_sent['Tweet'] for item in sublist])
temp_negative = pd.DataFrame(top.most_common(20))
temp_negative = temp_negative.iloc[1:,:]
temp_negative.columns = ['Common_words','count']

#Data cleaning
temp_negative['Common_words'] = temp_negative['Common_words'].map(lambda x: re.sub(r'\W+', '', x))
temp_negative['Common_words'] = temp_negative['Common_words'].replace(r'\W+', '', regex=True)
temp_negative=temp_negative[~temp_negative['Common_words'].isin(['s','t'])] #new line removing meaningless words from above
#mask1 = temp_negative.Common_words.str.contains('[a-zA-Z]')
#mask2 = temp_negative.Common_words.notna()
#temp_negative = temp_negative[mask1 | mask2]

temp_negative.Common_words =  temp_negative.Common_words.replace("", np.nan)
temp_negative = temp_negative.dropna(subset=['Common_words'])

temp_negative.style.background_gradient(cmap='Reds')

fig = px.bar(temp, x="count", y="Common_words", title='Commmon Words in Selected Text', orientation='h', 
             width=700, height=700,color='Common_words')
fig.show()

import numpy as np
top = Counter([item for sublist in Positive_sent['Tweet'] for item in sublist])
temp_positive = pd.DataFrame(top.most_common(23))
temp_positive.columns = ['Common_words','count']
temp_positive['Common_words'] = temp_positive['Common_words'].map(lambda x: re.sub(r'\W+', '', x))
temp_positive['Common_words'] = temp_positive['Common_words'].replace(r'\W+', '', regex=True)
temp_positive['Common_words'] = temp_positive['Common_words'].apply(lambda x:remove_spaces(x))
temp_positive=temp_positive[~temp_positive['Common_words'].isin(['s','gre','“',' * '])] #new line removing meaningless words
mask1 = temp_positive.Common_words.str.contains('[a-zA-Z]')
mask2 = temp_positive.Common_words.notna()
temp_positive = temp_positive[mask1 | mask2]
temp_positive.Common_words =  temp_positive.Common_words.str.replace(r"\s+", "").replace("", np.NaN)
temp_positive=temp_positive.dropna()


temp_positive.style.background_gradient(cmap='Greens')

fig = px.bar(temp, x="count", y="Common_words", title='Commmon Words in Selected Text', orientation='h', 
             width=700, height=700,color='Common_words')
fig.show()

# Commented out IPython magic to ensure Python compatibility.
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from tqdm import tqdm
from textblob import TextBlob
import re
import itertools
import datetime
import csv

# Download Wordnet through NLTK in python console:
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import unidecode
import string

from nltk.probability import FreqDist

import matplotlib.pyplot as plt
import seaborn as sns
import string
# %matplotlib inline
#from plotly import graph_objs as go
#import plotly.express as px
#import plotly.figure_factory as ff

#sentiment analyser packages

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC  
from sklearn.datasets import load_files
from sklearn.model_selection import GridSearchCV
import numpy as np
#import mglearn
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import f1_score, accuracy_score
from sklearn.metrics import roc_auc_score

def word_check(word, list):
    if word in list:
        return 1
    else:
        return 0
    
def word_cooccurance(word1,word2,candi_kw_lst):
    value = 0
    for k in range(len(candi_kw_lst)) :
        value  = value + check_both(word1,word2,candi_kw_lst[k])
    
    return value

def check_both(word1, word2 , list): 
    if word1 in list:
        if word2 in list:
            return 1
        else:
            return 0
    else:
        return 0
    
def word_freq(word,list1):
    return list1.count(word)
    

def strip_links(text):
    text = str(text)
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], '')    
    return text



def get_tweet_sentiment(tweet): 
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(clean_tweet(tweet)) 
    # set sentiment 
    if analysis.sentiment.polarity > 0: 
        return 'positive'
    elif analysis.sentiment.polarity == 0: 
        return 'neutral'
    else: 
        return 'negative'
    
def clean_tweet(tweet): 
    ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
    '''
    tweet = str(tweet)
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def textblob_sentiment(tweet):
    pol_score = TextBlob(tweet).sentiment.polarity
    if pol_score > 0: 
        return 'positive'
    elif pol_score == 0: 
        return 'neutral'
    else: 
        return 'negative'

def vader_sentiment(tweet):
    senti = SentimentIntensityAnalyzer()
    compound_score = senti.polarity_scores(tweet)['compound']
    
    # set sentiment 
    if compound_score >= 0.05: 
        return 'positive'
    elif (compound_score > -0.05) and (compound_score < 0.05): 
        return 'neutral'
    else: 
        return 'negative'
    



def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

stop_words = set(stopwords.words('english'))

appos = {
"aren't" : "are not",
"can't" : "cannot",
"couldn't" : "could not",
"didn't" : "did not",
"doesn't" : "does not",
"don't" : "do not",
"hadn't" : "had not",
"hasn't" : "has not",
"haven't" : "have not",
"he'd" : "he would",
"he'll" : "he will",
"he's" : "he is",
"i'd" : "i would",
"i'd" : "i had",
"i'll" : "i will",
"i'm" : "i am",
"isn't" : "is not",
"it's" : "it is",
"it'll":"it will",
"i've" : "i have",
"let's" : "let us",
"mightn't" : "might not",
"mustn't" : "must not",
"shan't" : "shall not",
"she'd" : "she would",
"she'll" : "she will",
"she's" : "she is",
"shouldn't" : "should not",
"that's" : "that is",
"there's" : "there is",
"they'd" : "they would",
"they'll" : "they will",
"they're" : "they are",
"they've" : "they have",
"we'd" : "we would",
"we're" : "we are",
"weren't" : "were not",
"we've" : "we have",
"what'll" : "what will",
"what're" : "what are",
"what's" : "what is",
"what've" : "what have",
"where's" : "where is",
"who'd" : "who would",
"who'll" : "who will",
"who're" : "who are",
"who's" : "who is",
"who've" : "who have",
"won't" : "will not",
"wouldn't" : "would not",
"you'd" : "you would",
"you'll" : "you will",
"you're" : "you are",
"you've" : "you have",
"'re": " are",
"wasn't": "was not",
"we'll":" will",
"didn't": "did not"
}



def text_preprocess(text):
    lemma = nltk.wordnet.WordNetLemmatizer()
    
    text = str(text)
    
    #removing mentions and hashtags

    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", text).split())
    
    #remove http links from tweets
    
    
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], '')  
    
    text_pattern = re.sub("`", "'", text)
    
    #fix misspelled words

    '''Here we are not actually building any complex function to correct the misspelled words but just checking that each character 
    should occur not more than 2 times in every word. It’s a very basic misspelling check.'''

    text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
    
    
   # print(text_pattern)
    
    #Convert to lower and negation handling
    
    text_lr = text_pattern.lower()
    
   # print(text_lr)
    
    words = text_lr.split()
    text_neg = [appos[word] if word in appos else word for word in words]
    text_neg = " ".join(text_neg) 
   # print(text_neg)
    
    #remove stopwords
    
    tokens = word_tokenize(text_neg)
    text_nsw = [i for i in tokens if i not in stop_words]
    text_nsw = " ".join(text_nsw) 
   # print(text_nsw)
    
    
    #remove tags
    
    text_tags=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text_nsw)

    # remove special characters and digits
    text_alpha=re.sub("(\\d|\\W)+"," ",text_tags)
    
    #Remove accented characters
    text = unidecode.unidecode(text_alpha)
    
    '''#Remove punctuation
    table = str.maketrans('', '', string.punctuation)
    text = [w.translate(table) for w in text.split()]'''
    
    sent = TextBlob(text)
    tag_dict = {"J": 'a', 
                "N": 'n', 
                "V": 'v', 
                "R": 'r'}
    words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in sent.tags]    
    lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
   
    return " ".join(lemmatized_list)

mario['processed_text'] = None
#train_df['clean_text2'] = None

for i in range(len(mario)):
    mario.processed_text[i] = text_preprocess(mario.text[i])

df['profile'].tail(2)

"""Word Cloud"""

# Commented out IPython magic to ensure Python compatibility.
#Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
from wordcloud import WordCloud
#Importing Dataset
#df = pd.read_csv("android-games.csv")
#Checking the Data
df.head()
#Checking for NaN values
df.isna().sum()
#Removing NaN Values
#df.dropna(inplace = True)
#Creating the text variable
text = " ".join(cat for cat in df['profile'])
# Creating word_cloud with text as argument in .generate() method
word_cloud = WordCloud(collocations = False, background_color = 'white').generate(text)
# Display the generated Word Cloud
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show()

df1=df['cat_pos'].iloc[0:98]
df1.tail(5)

df_cat_neg=pd.DataFrame(df_cat_neg)

df_cat_neg.tail(2)
