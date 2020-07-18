"""
Train the model and evaluate using test and cross-validation sets 
"""
from tensorflow import keras
from sentiment_model import SentimentModel
import matplotlib.pyplot as plt
import logging


class Train():  
    def __init__(self):
        """Initialize for training"""
        self.sentiment_obj = SentimentModel()
        self.model = self.sentiment_obj.get_model()
        self.X_train_indices, self.Y_train, self.X_val_indices,\
             self.Y_val, self.X_test_indices, self.Y_test = self.sentiment_obj.load_data()
          
    def train_model(self, epochs):
        """Train model"""

        # Compile model before training
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Define callbacks
        tensorboard_callback = keras.callbacks.TensorBoard(log_dir="src\logs")
        early_stoping = keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
        model_checkpoint = keras.callbacks.ModelCheckpoint('model\model_v2.h5', monitor='val_loss', mode='min', save_best_only=True)

        # Perform fitting
        history = self.model.fit(self.X_train_indices, self.Y_train,
                            epochs = epochs, batch_size = 32,
                            shuffle=True, callbacks=[tensorboard_callback, early_stoping, model_checkpoint],
                        validation_data = (self.X_val_indices, self.Y_val))
        
        # Evaluate model
        self.evaluate_model()

        return history

    def evaluate_model(self):
        """Evaluate trained model on test set"""

        logging.critical("--- Evaluating on Test set")
        loss, acc = self.model.evaluate(self.X_test_indices, self.Y_test)
        logging.critical(f"Test accuracy = {acc}")
        logging.critical(f"Test loss = {loss}")

    def plot_loss(self, history):
        """Plot training and cross-validation loss"""
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train','validation'], loc='upper left')
        # plt.savefig('notebook/img/loss_600dpi.png', dpi=600, bbox_inches='tight')
        plt.show()

    def plot_accuracy(self, history):
        """Plot training and cross-validation accuracy"""
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train','validation'], loc='upper left')
        # plt.savefig('notebook/img/accuracy_600dpi.png', dpi=600, bbox_inches='tight')
        plt.show()
               

if __name__ == "__main__":
    training = Train()
    # Number of epochs to train
    epochs = 2
    
    history = training.train_model(epochs)
    training.plot_loss(history)
    training.plot_accuracy(history)