import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from nltk.corpus import twitter_samples
import nltk
nltk.download('twitter_samples')

# Load Twitter data
positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')

# Combine positive and negative tweets
tweets = positive_tweets + negative_tweets

# Create labels
labels = np.concatenate([np.ones(len(positive_tweets)), np.zeros(len(negative_tweets))])

# Preprocess the data
tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')
tokenizer.fit_on_texts(tweets)
"""
fit_on_texts build a frequency vocab distribution so i will need to call this 
anyways. Not sure if i can use this keras tokenizer instead of the nlp one.

 we could manually create a dictionary (word_to_index)
 to map each word in the tokenizer's vocabulary to an integer.
  Then, for each tokenized tweet, we replace each token with its
   corresponding integer using the dictionary. 
"""
sequences = tokenizer.texts_to_sequences(tweets)
padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post')

# TD: need to convert our preproccecing data -> a tensor


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)



# Define the model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(5000, 16, input_length=100),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=5, batch_size=16, validation_data=(X_test, y_test))
 
# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print("Test Accuracy:", accuracy)
