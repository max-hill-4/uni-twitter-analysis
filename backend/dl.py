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
#[["hello this is a tweet!"], ]
tweets = positive_tweets + negative_tweets

vocab = []
count = 0


# Create labels
# numpy array of 1 or 0
labels = np.concatenate([np.ones(len(positive_tweets)), np.zeros(len(negative_tweets))])

# Creates vocab, of most popular 5000 words, use OOV if not in vocab.
# (word, index, frequency)
    
tweets = ["yo yo yo hello guys yes i am a real tweet ", "im the second tweet guys!"]
tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')

tokenizer.fit_on_texts(tweets)

#Vectorizes every tweet
sequences = tokenizer.texts_to_sequences(tweets)

# Makes every item of length 100 using 0 as padding
padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post')

print(padded_sequences)

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
