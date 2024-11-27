from textblob import TextBlob

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
