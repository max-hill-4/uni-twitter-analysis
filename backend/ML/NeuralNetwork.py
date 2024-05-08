from model import Model
from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
# installing a whole module from req is NOT worth man 😭😭😭
from sklearn.model_selection import train_test_split
from nltk.corpus import twitter_samples

class NeuralNetwork(Model):
    def _preprocess(self, tweets):
        
        # Build vocap map.
        tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')
        tokenizer.fit_on_texts(self.pos_data + self.neg_data)
        print(len(tokenizer.word_index))
        #Vectorizes every tweet.
        sequences = tokenizer.texts_to_sequences(tweets)
        print(sequences[0])
        # Pads every tweet.
        padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post')
        print(padded_sequences[0])
        return padded_sequences
        
    def _trainmodel(self, epochs:int= 5):
        
        padded_sequences = self._preprocess(self.pos_data + self.neg_data)
        labels = np.concatenate([np.ones(len(self.pos_data)), np.zeros(len(self.neg_data))])

        X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
        
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(5000, 16, input_length=100),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        # Compile the model
        model.compile (loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        # Train the model
        h = model.fit(X_train, y_train, epochs=epochs, batch_size=16, validation_data=(X_test, y_test))
        
        return h.history
        
    async def predict(self, tweet):
        print(f' predict is recieving: {tweet}')

        tweet = self._preprocess(tweet)
        model = tf.keras.models.load_model(r'backend\ML\models\NeuralNetwork.keras')

        values = model.predict(tweet)
        avg = np.mean(values)
        return 'p' if avg > 0.5 else 'n'
