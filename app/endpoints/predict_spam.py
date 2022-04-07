import logging
from pathlib import Path
from joblib import load
from fastapi import APIRouter, HTTPException, Depends

from app.endpoints.user import get_current_user
from app.ml_models.ml_model_trainer import MLModelTrainer
from app.models import User
from app.models.predict_spam import SpamRequest, SpamResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


cwd = Path.cwd()
spam_detect_pkl = cwd / "app" / 'ml_models' / 'spam_detector_model.pkl'
vectorizer_pickle = cwd / "app" / 'vectors' / "vectorizer.pickle"
if not spam_detect_pkl.exists() or not vectorizer_pickle.exists():
    trainer = MLModelTrainer()
    prepared_data = trainer.prepare_data("spam.csv")
    logger.debug("Spam data is prepared")
    vectorizer, model = trainer.create_train(prepared_data)
    logger.debug("Model was trained!")
    trainer.save_model(ml_model=model, vectorizer=vectorizer)
    logger.debug("Our machine model is trained and waiting for use")

# Load the ml_model
spam_clf = load(open(spam_detect_pkl, 'rb'))
# Load vectorizer
vectorizer = load(open(vectorizer_pickle, 'rb'))


router = APIRouter(tags=["predict_spam"])


@router.post("/predict_sentiment", status_code=200, response_model=SpamResponse)
def predict_spam(predict: SpamRequest, current_user: User = Depends(get_current_user)):
    logger.debug("Received message for analysis.")
    polarity = ""
    text_message = predict.text_message
    if not text_message:
        raise HTTPException(status_code=400, 
                            detail="Please Provide a valid text message")

    prediction = spam_clf.predict(vectorizer.transform([text_message]))

    if prediction[0] == 0:
        polarity = "Ham"

    elif prediction[0] == 1:
        polarity = "Spam"

    response = SpamResponse(
        text_message=text_message,
        spam_polarity=polarity
    )
    return response