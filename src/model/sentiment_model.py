import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from src.model.settings import embedding_dim, embeding_path, max_features
from src.utils.common import get_word_embedding_dictionary, sentences_to_indices 
import sys
import os

# Ignoring system gpu
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

class SentimentModel():  
    def __init__(self):
        self.word_to_index, self.index_to_word, self.word_to_vec_map = get_word_embedding_dictionary()

        # Define sentence_indices as the input of the graph.
        sentence_indices =layers.Input(shape=max_features, dtype="int32")
        
        # Create the embedding layer pretrained with GloVe Vectors
        embedding_layer = self.load_embedding_layer()
        
        embeddings = embedding_layer(sentence_indices)   
        x = layers.LSTM(50, return_sequences=True)(embeddings)
        x = layers.Dropout(0.4)(x)
        x = layers.BatchNormalization()(x)
        x = layers.LSTM(50)(x)
        x = layers.Dropout(0.4)(x)
        x = layers.BatchNormalization()(x)
        predictions = layers.Dense(1, activation="sigmoid", name="predictions")(x)
        
        # Create Model instance which converts sentence_indices into X.
        self.model = keras.Model(inputs=sentence_indices,outputs=predictions)        

    def get_model(self):
        return self.model

    def __repr__(self):
        return self.model.summary()

    def load_data(self):
        tweets = pd.read_csv("data/tweets_improved.csv")
        tweets_test = pd.read_csv("data/tweets_test.csv")
        X_train = tweets["tweet"]
        Y_train = tweets["sentiment"]
        X_val, X_test, Y_val, Y_test = train_test_split (tweets_test["tweet"],\
             tweets_test["sentiment"], test_size = 0.50, random_state = 1)

        X_train_indices = sentences_to_indices(X_train, self.word_to_index, max_features)
        X_val_indices = sentences_to_indices(X_val,self.word_to_index, max_features)
        X_test_indices = sentences_to_indices(X_test, self.word_to_index, max_features)

        return X_train_indices, Y_train, X_val_indices, Y_val, X_test_indices, Y_test

    def load_embedding_layer(self):
        # Adding 1 to fit Keras embedding (requirement)
        vocab_len = len(self.word_to_index) + 1                  

        emb_matrix = np.zeros((vocab_len,embedding_dim))
        for word, idx in self.word_to_index.items():
            emb_matrix[idx, :] = self.word_to_vec_map[word]

        embedding_layer = layers.Embedding(
                            vocab_len,
                            embedding_dim,
                            trainable = False
                            )

        # Build the embedding layer (required before setting the weights) 
        embedding_layer.build((None,))
        
        # Set the weights of the embedding layer to the embedding matrix.Layer is now pretrained.
        embedding_layer.set_weights([emb_matrix])
        
        return embedding_layer


