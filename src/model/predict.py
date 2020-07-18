from tensorflow.keras.models import load_model
from settings import active_model, max_features
from src.utils.common import sentences_to_indices, preprocess, get_word_embedding_dictionary
import numpy as np
import os

# Ignoring system gpu
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

class Predict():
    def __init__(self):
        """ Intialize active model and load word indices"""
        self.model = load_model(f"model/{active_model}.h5")
        self.word_to_index, _ , _ = get_word_embedding_dictionary()

    def get_sentiment(self, text):
        """ Evaluate sentiment from model output """
        text_indices = self.preprocess_text(text)
        prediction_array = self.model.predict(text_indices, batch_size=1, verbose = 0)[0]
        
        sentiment_data = self.get_sentiment_helper(prediction_array)
        return sentiment_data

    def preprocess_text(self, text):
        """ Preprocess text before sending to model"""
        
        # Preprocess text to remove urls, punctuations and user_mentions
        text = preprocess(text)

        # Creating array of sentence
        text_list = []
        text_list.append(text) 
        text_array = np.asarray(text_list)

        # Converting text to indices
        text_indices = sentences_to_indices(text_array, self.word_to_index, max_features)

        return text_indices

    def get_sentiment_helper(self, prediction_array):
        """ Define representation for sentiment """
        sentiment_data = {}

        if prediction_array[0] < 1:
            sentiment_data["sentiment"] = "Negative"
            sentiment_data["degree"] = round(prediction_array[0], 3)

        return sentiment_data
        
