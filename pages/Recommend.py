import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.helper import load_data


df = load_data()

st.title("🤖 Book Recommender & Bestseller Predictor")
st.markdown("Search for a book to get similar recommendations — or check if any book could be the next bestseller.")
st.markdown("---")

# ════════════════════════════════════════════════════════
# SECTION 1 — Book Recommender
# ════════════════════════════════════════════════════════
st.subheader("📚 Get Book Recommendations")

col1, col2 = st.columns([3, 1])
with col1:
    book_input = st.text_input("Type a book name you like", placeholder="e.g. Harry Potter")
with col2:
    num_recs = st.selectbox("How many recommendations?", [5, 10, 15], index=0)

if st.button("🔍 Find Recommendations", use_container_width=True):
    if not book_input.strip():
        st.warning("Please enter a book name.")
    else:
        matched = df[df["title"].str.contains(book_input.strip(), case=False, na=False)]

        if matched.empty:
            st.error(f"❌ No book found matching **'{book_input}'**. Try a different title.")
        else:
            found = matched.iloc[0]
            genre = found["genre"]

            st.success(f"✅ Found: **{found['title']}** by {found['authors']} | Genre: **{genre}** | ⭐ {found['average_rating']}")

            if pd.isna(genre):
                st.warning("Genre not available for this book — can't recommend similar titles.")
            else:
                recs = df[
                    (df["genre"] == genre) &
                    (~df["title"].str.contains(book_input.strip(), case=False, na=False))
                ].sort_values(
                    by=["recommendation_score", "average_rating"],
                    ascending=False
                ).head(num_recs)

                st.markdown(f"#### 📖 Top {num_recs} books similar to *{found['title']}* in **{genre}**")
                st.dataframe(
                    recs[["title", "authors", "average_rating", "ratings_count",
                          "trend_tier", "is_bestseller"]]
                    .rename(columns={
                        "title": "Title", "authors": "Author",
                        "average_rating": "Rating", "ratings_count": "Reviews",
                        "trend_tier": "Trend", "is_bestseller": "Bestseller?"
                    })
                    .reset_index(drop=True),
                    use_container_width=True
                )

st.markdown("---")

# ════════════════════════════════════════════════════════
# SECTION 2 — Browse by Genre
# ════════════════════════════════════════════════════════
st.subheader("🎭 Browse Top Books by Genre")

genre_pick = st.selectbox("Choose a genre", sorted(df["genre"].unique()))
sort_by = st.radio("Sort by", ["Rating", "Popularity", "Bestseller Probability"], horizontal=True)

sort_map = {
    "Rating":                 "average_rating",
    "Popularity":             "popularity_score",
    "Bestseller Probability": "bestseller_probability"
}

genre_books = df[df["genre"] == genre_pick].sort_values(
    sort_map[sort_by], ascending=False
).head(15)

st.dataframe(
    genre_books[["title", "authors", "average_rating", "ratings_count",
                 "bestseller_probability", "trend_tier", "is_bestseller"]]
    .rename(columns={
        "title": "Title", "authors": "Author",
        "average_rating": "Rating", "ratings_count": "Reviews",
        "bestseller_probability": "Bestseller Prob (%)",
        "trend_tier": "Trend", "is_bestseller": "Bestseller?"
    })
    .reset_index(drop=True),
    use_container_width=True
)

st.markdown("---")

# ════════════════════════════════════════════════════════
# SECTION 3 — Bestseller Predictor
# ════════════════════════════════════════════════════════
st.subheader("🎯 Will This Book Become a Bestseller?")
st.markdown("Enter the details of any book and we'll predict its bestseller probability.")

with st.form("predictor_form"):
    pc1, pc2 = st.columns(2)
    with pc1:
        avg_rating   = st.slider("Average Rating",       1.0, 5.0, 4.0, 0.1)
        ratings_cnt  = st.number_input("Ratings Count",  min_value=0, value=5000, step=500)
    with pc2:
        reviews_cnt  = st.number_input("Text Reviews",   min_value=0, value=500, step=50)
        trend_score  = st.slider("Trend Score",          0.0, 100.0, 50.0, 0.5)

    rec_score = st.slider("Recommendation Score",        0.0, 100.0, 50.0, 0.5)
    submitted = st.form_submit_button("🔮 Predict Bestseller Chance", use_container_width=True)

if submitted:
    # Simple weighted scoring using the same features as the ML model
    # Weights derived from feature importance order: ratings_count > reviews > trend > rating > rec
    score = (
        (min(ratings_cnt, 500000) / 500000) * 40 +
        (min(reviews_cnt, 50000)  / 50000)  * 25 +
        (trend_score / 100)                  * 20 +
        ((avg_rating - 1) / 4)               * 10 +
        (rec_score / 100)                    * 5
    )
    probability = round(score, 1)

    st.markdown("---")
    col_r1, col_r2 = st.columns([1, 2])
    with col_r1:
        if probability >= 65:
            st.success(f"### 🏆 {probability}%\nHigh chance of becoming a bestseller!")
        elif probability >= 40:
            st.warning(f"### 📈 {probability}%\nModerate bestseller potential.")
        else:
            st.error(f"### 📉 {probability}%\nLow bestseller probability right now.")

    with col_r2:
        st.markdown("**What influences bestseller status most:**")
        st.markdown(f"- 📊 Ratings Count contributes **40%** → yours: `{ratings_cnt:,}`")
        st.markdown(f"- 💬 Text Reviews contributes **25%** → yours: `{reviews_cnt:,}`")
        st.markdown(f"- 🔥 Trend Score contributes **20%** → yours: `{trend_score}`")
        st.markdown(f"- ⭐ Average Rating contributes **10%** → yours: `{avg_rating}`")
        st.markdown(f"- 🎯 Rec Score contributes **5%** → yours: `{rec_score}`")