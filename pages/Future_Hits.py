import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.helper import load_data


df = load_data()

st.title("🔮 Future Hits")
st.markdown("Books predicted to become the next bestsellers based on trend scores and ML prediction.")
st.markdown("---")

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)
k1.metric("🔮 Predicted Next Bestsellers", f"{df['predicted_bestseller_next_month'].sum():,}")
k2.metric("🔥 Currently Trending",         f"{df['is_trending_now'].sum():,}")
k3.metric("📈 Avg Next Bestseller Score",  f"{df['next_bestseller_score'].mean():.1f}")

st.markdown("---")

# ── Top 10 future hits table ───────────────────────────────────────────────────
st.subheader("🏅 Top 10 Books Most Likely to be Next Bestsellers")
future = df[df["is_bestseller"] == 0].sort_values("next_bestseller_score", ascending=False).head(10)
st.dataframe(
    future[["title", "authors", "genre", "average_rating",
            "next_bestseller_score", "bestseller_probability", "trend_tier"]]
    .reset_index(drop=True),
    use_container_width=True
)

st.markdown("---")

# ── Charts Row ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Genres with Highest Future Bestseller Potential")
    genre_future = df.groupby("genre")["next_bestseller_score"].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=genre_future.values, y=genre_future.index, palette="plasma", ax=ax)
    ax.set_xlabel("Avg Next Bestseller Score")
    ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("📈 Trend Score vs Bestseller Probability")
    sample = df.sample(min(1000, len(df)), random_state=42)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=sample, x="trend_score", y="bestseller_probability",
                    hue="trend_tier", alpha=0.6, ax=ax)
    ax.set_xlabel("Trend Score")
    ax.set_ylabel("Bestseller Probability (%)")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ── Filter & Explore ───────────────────────────────────────────────────────────
st.subheader("🔍 Explore by Genre")
genres = sorted(df["genre"].unique())
selected_genre = st.selectbox("Pick a genre", genres)

genre_df = df[df["genre"] == selected_genre].sort_values("next_bestseller_score", ascending=False)

col3, col4 = st.columns(2)
col3.metric("Books in Genre",       f"{len(genre_df):,}")
col4.metric("Avg Future Score",     f"{genre_df['next_bestseller_score'].mean():.1f}")

st.dataframe(
    genre_df[["title", "authors", "average_rating", "next_bestseller_score",
              "trend_tier", "prediction_confidence"]].head(20).reset_index(drop=True),
    use_container_width=True
)