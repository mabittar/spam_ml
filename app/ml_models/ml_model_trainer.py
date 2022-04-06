import os
import sys
from pathlib import Path
import joblib

from app.ml_models.data_processor import prepare_data, create_train_test_data
from app.ml_models.model_trainer import run_model_training


class MLModelTrainer:
    def __init__(self):
        self.cwd = Path.cwd()
        
    def prepare_data(self, file_name: str):
        # 0.Path to data
        raw_data = self.cwd / "app" / 'data' / file_name
        if not raw_data.exists():
            print("raw data not found. Stop!")
            sys.exit("File not found!")
        # 1.Prepare the data
        prepared_data = prepare_data(raw_data, encoding="latin-1")
        return prepared_data

    @staticmethod
    def create_train(data):
        # 2.Create train - test split
        train_test_data, vectorizer = create_train_test_data(
            data['text'], data['label'], 0.33, 2021
        )

        # 3.Run training
        ml_model = run_model_training(
            train_test_data['x_train'],
            train_test_data['x_test'],
            train_test_data['y_train'],
            train_test_data['y_test']
        )
        return vectorizer, ml_model
    
    def save_model(self, ml_model, vectorizer):
        # 4.Save the trained model and vectorizer
        spam_detect_pkl = self.cwd / "app" / 'ml_models' / 'spam_detector_model.pkl'
        if spam_detect_pkl.exists():
            os.remove(spam_detect_pkl)
        joblib.dump(ml_model, spam_detect_pkl)

        vectorizer_pickle = self.cwd / "app" / 'vectors' / "vectorizer.pickle"
        if spam_detect_pkl.exists():
            os.remove(spam_detect_pkl)
        joblib.dump(vectorizer, open(vectorizer_pickle, "wb"))
   
        
if __name__ == '__main__':
    trainer = MLModelTrainer()
    prepared_data = trainer.prepare_data("spam.csv")
    print("Spam data is prepared")
    vectorizer, model = trainer.create_train(prepared_data)
    print("Model was trained!")
    trainer.save_model(ml_model=model, vectorizer=vectorizer)
    print("Our machine model is trained and wainting for use")
    