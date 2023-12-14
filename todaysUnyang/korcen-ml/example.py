#py: 3.10, tf: 2.10
#kogpt2
import tensorflow as tf
import numpy as np
import pickle
from keras.utils import pad_sequences

maxlen = 1000 # 모델마다 값이 다름

model_path = 'todaysUnyang\\korcen-ml\\vdcnn_model_with_kogpt2.h5'
tokenizer_path = "todaysUnyang\\korcen-ml\\tokenizer_with_kogpt2.pickle"

model = tf.keras.models.load_model(model_path)
with open(tokenizer_path, "rb") as f:
    tokenizer = pickle.load(f)

def preprocess_text(text):
    text = text.lower()
    
    return text

def predict_text(text):
    sentence = preprocess_text(text)
    encoded_sentence = tokenizer.encode_plus(sentence,
                                             max_length=maxlen,
                                             padding="max_length",
                                             truncation=True)['input_ids']
    sentence_seq = pad_sequences([encoded_sentence], maxlen=maxlen, truncating="post")
    prediction = model.predict(sentence_seq)[0][0]
    return prediction
    
def is_safe_word(text):
    result = predict_text(text)
    if result >= 0.5:
        print("불량 언어 감지")
        return False
    else:
        return True