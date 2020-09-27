# Sentiment App
The sentiment app runs on a Recurrent Neural Network (RNN) to classify a sentence into positive or negative classes.

Labelled Twitter tweets were used to train the model. 
    To extract Twitter tweets Twitter Search API was used. 
    https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets

Stanford GloVe Twitter word embedding have been used to vectorize words.

The model performs best on phrases with words more than 4 words.

Current running accuracy is about *85%*.

Code for the model can be found in src or as in notebooks folder.

