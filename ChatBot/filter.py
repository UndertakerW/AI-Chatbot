import nltk
import joblib
from nltk.tokenize import RegexpTokenizer, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from PyQt5.QtCore import QFileInfo
root = QFileInfo(__file__).absolutePath()
df = pd.read_csv(root+'\\spam.csv', encoding='ISO-8859-1')

data = df.to_numpy()

X = data[:, 1]  # X stores text emails
tokenizer = RegexpTokenizer('\w+')
nltk.download('stopwords')
sw = set(stopwords.words('english'))  # ignore the stop words in english
ps = PorterStemmer()


def getStem(str):
    str = str.lower()  # returns lowercased string from given string
    # splits string into substrings of words
    tokens = tokenizer.tokenize(str)
    # stopwords are removed
    removed_stopwords = [w for w in tokens if w not in sw]
    # tokens  are reduced into root form
    stemmed_words = [ps.stem(token) for token in removed_stopwords]
    # join all stemmed words to single string
    clean_review = ' '.join(stemmed_words)
    return clean_review


def getDoc(document):
    d = []
    for doc in document:
        d.append(getStem(doc))
    return d


stemmed_doc = getDoc(X)

cv = CountVectorizer()
vc = cv.fit_transform(stemmed_doc)


def update(emails):
    up = getDoc(emails)
    return cv.transform(up)


def filterEmail(email):
    # 多段文本转换成一行字符串
    email = ' '.join(email.split())

    model = joblib.load(root+"\\filter_model.m")
    
    emails = []

    emails.append(email)

    emails = update(emails)


    y_pred = model.predict(emails)

    return y_pred[0]  # the return value type is <class 'numpy.str_'>

