import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.helper import load_data


df = load_data()

st.title("💎 Hidden Gems")
st.markdown("Highly rated books that most people haven't discovered yet — low ratings count but excellent quality.")
st.markdown("---")

# ── Sliders to define a gem ────────────────────────────────────────────────────
st.subheader("⚙️ Define what counts as a Hidden Gem")
col1, col2 = st.columns(2)
with col1:
    min_rating = st.slider("Minimum Average Rating", 3.0, 5.0, 4.3, step=0.1)
with col2:
    max_reviews = st.slider("Maximum Ratings Count (less = more hidden)", 100, 10000, 2000, step=100)

gems = df[(df["average_rating"] >= min_rating) & (df["ratings_count"] <= max_reviews)]

st.markdown("---")

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)
k1.metric("💎 Hidden Gems Found",   f"{len(gems):,}")
k2.metric("⭐ Avg Rating",           f"{gems['average_rating'].mean():.2f}" if len(gems) else "—")
k3.metric("📖 Avg Pages",           f"{gems['num_pages'].mean():.0f}" if len(gems) else "—")

st.markdown("---")

if gems.empty:
    st.warning("No books match your criteria. Try lowering the minimum rating or increasing the max reviews count.")
else:
    # ── Top Gems Table ─────────────────────────────────────────────────────────
    st.subheader(f"🏅 Top Hidden Gems (sorted by rating)")
    st.dataframe(
        gems[["title", "authors", "genre", "average_rating", "ratings_count", "publication_year"]]
        .sort_values("average_rating", ascending=False)
        .reset_index(drop=True)
        .head(30),
        use_container_width=True
    )

    st.markdown("---")

    # ── Charts ─────────────────────────────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📚 Hidden Gems by Genre")
        gem_genres = gems["genre"].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(x=gem_genres.values, y=gem_genres.index, palette="YlGnBu", ax=ax)
        ax.set_xlabel("Number of Hidden Gems")
        ax.set_ylabel("")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col4:
        st.subheader("⭐ Rating Distribution of Hidden Gems")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.histplot(gems["average_rating"], bins=20, kde=True,
                     color="#7F77DD", ax=ax)
        ax.set_xlabel("Average Rating")
        ax.set_ylabel("Count")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")

    # ── Genre filter ───────────────────────────────────────────────────────────
    st.subheader("🔍 Filter Hidden Gems by Genre")
    selected = st.selectbox("Genre", sorted(gems["genre"].unique()))
    genre_gems = gems[gems["genre"] == selected].sort_values("average_rating", ascending=False)
    st.dataframe(
        genre_gems[["title", "authors", "average_rating", "ratings_count", "publication_year"]]
        .reset_index(drop=True).head(20),
        use_container_width=True
    )