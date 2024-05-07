from .model import Model
from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

from numpy import mean
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
# installing a whole module from req is NOT worth man 😭😭😭
from sklearn.model_selection import train_test_split
import numpy as np

class NeuralNetwork(Model):
    def _preprocess(self, tweets):
        """
        Builds a vocab map from vectorising every tweet in the test data.
        Args:
            tweets (list(str)): The list of tweets that need vectorising
        Returns:
            padded_sequences(list(int)) : Every tweet vectorised and standadized length
        """
        # Build vocap map.
        tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')
        tokenizer.fit_on_texts(self.pos_data + self.neg_data)

        #Vectorizes every tweet.
        sequences = tokenizer.texts_to_sequences(tweets)

        # Pads every tweet.
        padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post')
        return padded_sequences
        
    def _trainmodel(self):
        """
        Using tensowflows keras model, using two dense ReLU activation functions, and
        a sigmoid output layer.
        Returns a model as NeuralNetwork.keras
        """
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
        model.fit(X_train, y_train, epochs=7, batch_size=16, validation_data=(X_test, y_test))
        model.save(r'backend\ML\models\NeuralNetwork.keras')

    async def predict(self, tweet):
        """
        By using the trained keras file in models, classify a single tweet
        Args:
            tweet (str) : text data inside of tweet.
        Returns:
            'p' to indicate positive and 'n' to indicate negative
        """
        print(f' predict is recieving: {tweet}')

        tweet = self._preprocess(tweet)
        model = tf.keras.models.load_model(r'backend\ML\models\NeuralNetwork.keras')

        values = model.predict(tweet)
        avg = mean(values)
        return 'p' if avg > 0.5 else 'n'
