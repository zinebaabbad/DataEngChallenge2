#Import packages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import string
import re
import nltk



def preprocessing(article):
    #Convert each article to all lower case
    article=article.lower()
    # Remove punctations
    table = str.maketrans('', '', string.punctuation)
    article=article.translate(table)
    #remove numbers
    article = re.sub(r'\d+', 'num', article)
    #Remove stop words
    stopwords = set(nltk.corpus.stopwords.words('english') + ['The guardian']) #the guarddian is a word found at the end of the articles
    article_words = [word for word in article.split() if word not in stopwords]
    #stemming Many words with similar semantic meanings have different endings depending on the context
    stemmer = nltk.stem.PorterStemmer()
    article = " ".join([stemmer.stem(word) for word in article_words])

    return article



#Get nb similar documents to  query
def get_similarity(query, corpus, nb = 5): # by default returs 5 first results
    # prerocess and clean corpus and query
    corpus_preprocessed = [preprocessing(article) for article in corpus ]
    query=preprocessing(query)
    # init tfid object
    tfidf_vectorizer = TfidfVectorizer()
    # vectorize corpus and query
    tfidf_desc = tfidf_vectorizer.fit_transform(corpus_preprocessed)
    query = tfidf_vectorizer.transform([query])
    #find most similar vector
    cs = cosine_similarity(query, tfidf_desc)
    res= cs[0]
    result_list = [] #to stock index
    # get five most pert result
    while nb > 0:
        index = np.argmax(res)
        result_list.append(index)
        res[index] = 0
        nb = nb - 1

    return result_list




