import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_books.csv")
    df.drop_duplicates(inplace=True)
    df.fillna({
        "average_rating": 0,
        "ratings_count": 0,
        "text_reviews_count": 0,
        "trend_score": 0,
        "recommendation_score": 0,
        "next_bestseller_score": 0,
        "bestseller_probability": 0,
    }, inplace=True)
    df.dropna(subset=["title", "genre", "authors"], inplace=True)
    return df