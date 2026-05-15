# 📚 BookLens — Book Analytics & Prediction Platform

> A data analytics web app that explores book trends, predicts future bestsellers, discovers hidden gems, and recommends books based on user preferences.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red?style=flat-square&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green?style=flat-square&logo=pandas)
![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-ML%20Model-orange?style=flat-square&logo=scikit-learn)

---

## 🚀 Features

| Page | Description |
|------|-------------|
| 🏠 **Home** | Landing page with login/signup and navigation cards |
| 📊 **Dashboard** | Genre trends, ratings, bestseller stats and charts |
| 🔮 **Future Hits** | ML-predicted next bestsellers by trend & score |
| 💎 **Hidden Gems** | Highly rated books with low popularity (undiscovered) |
| 🤖 **Recommend** | Book recommender + interactive bestseller predictor |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Data Analysis:** Pandas, NumPy
- **Visualisation:** Matplotlib, Seaborn
- **Machine Learning:** Scikit-Learn (Random Forest)
- **Hypothesis Testing:** SciPy
- **Authentication:** SQLite + SHA-256 password hashing
- **Dataset:** 10,968 books across multiple genres

---

## 📁 Project Structure

```
BookLens/
│
├── app.py                  # Main entry point (login + page router)
├── auth.py                 # Authentication logic (SQLite)
│
├── pages/
│   ├── Dashboard.py        # Analytics dashboard
│   ├── Future_Hits.py      # Future bestseller predictions
│   ├── Gems.py             # Hidden gems explorer
│   └── Recommend.py        # Book recommender & predictor
│
├── utils/
│   └── helper.py           # Shared data loader
│
├── data/
│   └── cleaned_books.csv   # Dataset (10,968 books, 85 features)
│
├── models/
│   └── bestseller_model.pkl  # Trained Random Forest model
│
├── notebooks/
│   └── analysis.ipynb      # Full EDA + hypothesis testing notebook
│
└── requirements.txt
```

---

## ⚙️ Setup & Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/booklens.git
cd booklens
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Open in browser
```
http://localhost:8501
```

> On first run, create an account on the Sign Up page. User data is stored locally in `data/users.db`.

---

## 📊 Dataset

The dataset contains **10,968 books** with **85 features** including:
- Book metadata (title, author, genre, publisher, pages)
- Rating & review metrics
- Trend scores and tiers
- Bestseller labels and probability scores
- ML-generated prediction columns

---

## 🔍 Key Findings

1. **Literary Fiction** dominates the dataset with 7,317 books
2. **Review count** is the strongest predictor of bestseller status
3. **High ratings alone** do not guarantee bestseller status
4. Some low-popularity books are **hidden gems** with ratings above 4.5
5. **Random Forest** achieves strong accuracy in predicting bestsellers

---

## 👥 Team

Built as a Data Analytics college project.

---

## 📄 License

This project is for educational purposes only.
