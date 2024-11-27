import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from wordcloud import WordCloud
from datetime import datetime

# Database setup
class DatabaseHandler:
    def __init__(self, db_name="feedback.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            feedback_comment TEXT,
            sentiment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_feedback(self, name, comment, sentiment):
        query = """
        INSERT INTO feedback (name, feedback_comment, sentiment)
        VALUES (?, ?, ?)
        """
        self.conn.execute(query, (name, comment, sentiment))
        self.conn.commit()

    def fetch_all_feedback(self):
        query = "SELECT * FROM feedback"
        return self.conn.execute(query).fetchall()

# Sentiment analysis
class SentimentAnalysis:
    @staticmethod
    def analyze_sentiment(comment):
        analysis = TextBlob(comment)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            return "Positive"
        elif polarity < 0:
            return "Negative"
        else:
            return "Neutral"

# Initialize database
db = DatabaseHandler()

# Streamlit app
st.title("Customer Feedback Analysis Dashboard")

# Feedback Form
st.header("Submit Your Feedback")
name = st.text_input("Name")
feedback = st.text_area("Your Feedback")
if st.button("Submit Feedback"):
    if name and feedback:
        # Analyze sentiment
        sentiment = SentimentAnalysis.analyze_sentiment(feedback)
        # Save to database
        db.insert_feedback(name, feedback, sentiment)
        st.success(f"Thank you, {name}! Your feedback was classified as: {sentiment}")
    else:
        st.error("Please provide both name and feedback!")

# Dashboard
st.header("Feedback Dashboard")
feedback_data = db.fetch_all_feedback()

if feedback_data:
    # Convert feedback data to DataFrame
    df = pd.DataFrame(feedback_data, columns=["ID", "Name", "Feedback", "Sentiment", "Timestamp"])

    # Sidebar filters
    st.sidebar.header("Filters")
    sentiment_filter = st.sidebar.multiselect("Filter by Sentiment", ["Positive", "Neutral", "Negative"], default=["Positive", "Neutral", "Negative"])
    date_filter = st.sidebar.date_input("Filter by Date", [])

    # Apply filters
    if sentiment_filter:
        df = df[df["Sentiment"].isin(sentiment_filter)]
    if date_filter:
        df = df[pd.to_datetime(df["Timestamp"]).dt.date == date_filter]

    st.dataframe(df)

    # Sentiment Pie Chart
    st.subheader("Sentiment Distribution")
    sentiment_counts = df["Sentiment"].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", colors=["#76c893", "#f94144", "#f9c74f"])
    st.pyplot(plt)

    # Word Cloud
    st.subheader("Word Cloud of Feedback")
    all_feedback = " ".join(df["Feedback"])
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_feedback)
    st.image(wordcloud.to_array())

    # Feedback Trends
    st.subheader("Feedback Trends Over Time")
    df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
    trend_data = df.groupby("Date")["Sentiment"].value_counts().unstack().fillna(0)
    st.bar_chart(trend_data)

    # Export to CSV
    st.sidebar.header("Admin Options")
    if st.sidebar.button("Export Feedback to CSV"):
        df.to_csv("feedback_data.csv", index=False)
        st.sidebar.success("Data exported to feedback_data.csv")
else:
    st.info("No feedback submitted yet.")

