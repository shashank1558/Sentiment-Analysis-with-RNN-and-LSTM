"""Common utility functions"""
from textblob import TextBlob
import re
import preprocessor as pre
import json
import logging
import wordninja
from src.model.settings import embeding_path, embedding_dim
import numpy as np

class Tweet:
    """Holds tweet object"""
    def __init__(self, text, id_str, created_at, sentiment):
        self.tweet = text
        self.id = id_str
        self.created_at = created_at
        self.sentiment = sentiment

    def get_tweet(self):
        return f"{self.id},{self.created_at},{self.sentiment},{self.tweet}"
        
    def __str__(self):
        return f"{self.id},{self.created_at},{self.sentiment},{self.tweet}"

    def __repr__(self):
        return json.dumps({
            "id":self.id,
            "created_at":self.created_at,
            "sentiment":self.sentiment,
            "tweet":self.tweet
        })

        
def preprocess(text):
    """Preprocess text"""
    
    # Decode in utf8
    text = text.encode('utf-8', 'replace').decode()

    # Remove HTML tags
    text = re.sub("<[^>]*>","",text)

    # Remove URLs and user mentions
    pre.set_options(pre.OPT.URL, pre.OPT.MENTION)
    text = pre.clean(text)

    # Remove "#" character from hashtags(retaining hashtag content)
    text = re.sub("#"," ",text)

    # Get list of words, remove punctuation marks and convert ro lowercase
    text_blob = TextBlob(text)    
    text = text_blob.stripped.lower()

    # Remove anything that is not an alphabet or a number
    text = re.sub('[^a-z\s]','',text)
    
    return text
    
def calculate_sentiment(text):
    text_blob = TextBlob(text)
    polarity = text_blob.sentiment.polarity

    # 1-> positive
    # 0-> negative
    if polarity > 0:
        return 1
    return 0

def extract_tweet_features(tweet_dict):
    
    id_str = tweet_dict.get("id")
    created_at = tweet_dict.get("created_at")
    text= None
    try:
        text = preprocess(tweet_dict.get("full_text"))
    except Exception as e:
        logging.error(e)
        logging.error(tweet_dict.get("full_text"))
    sentiment = calculate_sentiment(text)

    # Creating tweet object
    tweet = Tweet(text, id_str, created_at, sentiment)
    return tweet


def get_word_embedding_dictionary():
    """ creates word_to_vector, word_to_index and index_to_word dictionaries """
    with open(embeding_path, "r", encoding="utf-8") as f:
        words = set()
        word_to_vec_map = {}
        skip_count = 0
        
        # Extracting word and its vectors
        for line in f:
            line_list = line.split()
            
            # Ignoring unresolvable words
            if len(line_list)!=embedding_dim+1:
                skip_count +=1
                continue
            curr_word = line_list[0]
            words.add(curr_word)
            word_to_vec_map[curr_word] = np.array(line_list[1:], dtype=np.float64)
            
        word_to_index = {}
        index_to_word = {}
        for i,w in enumerate(sorted(words)):
            word_to_index[w] = i
            index_to_word[i] = w
    return word_to_index, index_to_word, word_to_vec_map


def sentences_to_indices(X, word_to_index, max_len):
    """
    Covert words to indices before feeding to model
    """
    m = X.shape[0]                                   
    
    X_indices = np.zeros((m,max_len))
    
    # Assign indices to words
    for i,sentence in enumerate(X):        
        sentence_words = sentence.lower().split()
        sentence_words = sentence_words[:max_len]
        for j,word in enumerate(sentence_words):
            X_indices[i, j] = word_to_index.get(word,0)
    return X_indices