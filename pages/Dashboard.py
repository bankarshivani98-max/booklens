import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.helper import load_data


df = load_data()

st.title("📊 Dashboard")
st.markdown("A full overview of the book dataset — genres, ratings, trends and bestsellers.")
st.markdown("---")

# ── KPI Row ────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("📚 Total Books",      f"{len(df):,}")
k2.metric("🏆 Bestsellers",      f"{df['is_bestseller'].sum():,}")
k3.metric("⭐ Avg Rating",        f"{df['average_rating'].mean():.2f}")
k4.metric("🔥 Trending Now",     f"{df['is_trending_now'].sum():,}")

st.markdown("---")

# ── Row 1: Genre counts + Trend tier ──────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📚 Top 10 Genres by Book Count")
    genre_counts = df["genre"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette="viridis", ax=ax)
    ax.set_xlabel("Number of Books")
    ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("📈 Trend Tier Distribution")
    tier_counts = df["trend_tier"].value_counts()
    colors = ["#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff"]
    fig, ax = plt.subplots(figsize=(7, 4))
    tier_counts.plot(kind="bar", color=colors, ax=ax, edgecolor="white")
    ax.set_xlabel("Trend Tier")
    ax.set_ylabel("Number of Books")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ── Row 2: Highest rated genres + Bestsellers by genre ────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("⭐ Highest Rated Genres")
    genre_rating = df.groupby("genre")["average_rating"].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=genre_rating.values, y=genre_rating.index, palette="coolwarm", ax=ax)
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col4:
    st.subheader("🏆 Bestsellers by Genre")
    genre_bs = df[df["is_bestseller"] == 1]["genre"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=genre_bs.values, y=genre_bs.index, palette="Set2", ax=ax)
    ax.set_xlabel("Number of Bestsellers")
    ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ── Row 3: Scatter + Genre pie ─────────────────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.subheader("🔵 Ratings Count vs Average Rating")
    top_genres = df["genre"].value_counts().head(6).index
    plot_df = df[df["genre"].isin(top_genres)]
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=plot_df, x="ratings_count", y="average_rating",
                    hue="genre", alpha=0.5, ax=ax)
    ax.set_xscale("log")
    ax.set_xlabel("Ratings Count (log scale)")
    ax.set_ylabel("Average Rating")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col6:
    st.subheader("🥧 Genre Distribution")
    genre_counts_pie = df["genre"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.pie(genre_counts_pie.values, labels=genre_counts_pie.index,
           autopct="%1.1f%%", startangle=140)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ── Bestseller Probability by Genre ───────────────────────────────────────────
st.subheader("🎯 Bestseller Probability by Genre")
bs_prob = df.groupby("genre")["bestseller_probability"].mean().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(12, 4))
sns.barplot(x=bs_prob.values, y=bs_prob.index, palette="magma", ax=ax)
ax.set_xlabel("Avg Bestseller Probability (%)")
ax.set_ylabel("")
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ── Raw Data Explorer ─────────────────────────────────────────────────────────
with st.expander("🔍 Explore Raw Data"):
    genre_filter = st.multiselect("Filter by Genre", options=sorted(df["genre"].unique()),
                                   default=list(df["genre"].value_counts().head(3).index))
    filtered = df[df["genre"].isin(genre_filter)] if genre_filter else df
    st.dataframe(
        filtered[["title", "authors", "genre", "average_rating",
                  "ratings_count", "is_bestseller", "trend_tier"]].head(100),
        use_container_width=True
    )