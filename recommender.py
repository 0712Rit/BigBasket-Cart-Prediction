from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def create_similarity_matrix(df):
    df["text"] = df["product"] + " " + df["category"] + " " + df["brand"]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["text"])
    sim_matrix = cosine_similarity(tfidf_matrix)
    return sim_matrix

def recommend_products(df, sim_matrix, product_name, top_n=5):
    idx = df[df["product"].str.lower() == product_name.lower()].index
    if len(idx) == 0:
        return ["Product not found in dataset."]
    idx = idx[0]
    scores = list(enumerate(sim_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended = [df.iloc[i[0]]["product"] for i in scores]
    return recommended
