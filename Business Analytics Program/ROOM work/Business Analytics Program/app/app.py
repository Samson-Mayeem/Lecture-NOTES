from flask import Flask, render_template
import pandas as pd
from textblob import TextBlob
from collections import Counter

app = Flask(__name__)

def perform_sentiment_analysis(review):
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    themes = []

    if isinstance(review, str):
            analysis = TextBlob(review)
            sentiment = analysis.sentiment.polarity

            if sentiment > 0:
                positive_count += 1
            elif sentiment < 0:
                negative_count += 1
            else:
                neutral_count += 1

            nouns = [word for (word, pos) in analysis.tags if pos[0] == 'N']
            themes.extend(nouns)

    total_reviews = len(review)
    positive_percentage = (positive_count / total_reviews) * 100
    negative_percentage = (negative_count / total_reviews) * 100
    neutral_percentage = (neutral_count / total_reviews) * 100

    common_themes = [theme for theme, _ in Counter(themes).most_common(5)]

    report = {
        'Total Reviews': total_reviews,
        'Positive Sentiment (%)': positive_percentage,
        'Negative Sentiment (%)': negative_percentage,
        'Neutral Sentiment (%)': neutral_percentage,
        'Common Themes': common_themes
    }

    return report

@app.route('/')
def index():
    # Read reviews from Excel file
    try:
        df = pd.read_excel('mcdonalds_data.xlsx', engine='openpyxl')
    except FileNotFoundError:
        return render_template('error.html', message='File not found')

    # Print all column names
    print("All column names and their indices:")
    for idx, col_name in enumerate(df.columns):
        print(f"{idx}: {col_name}")

    # Check if 'review' column is present
    if 'review' not in df.columns:
        return render_template('error.html', message='Missing "review" column in the Excel file')

    reviews = df['review'].tolist()

    # Perform sentiment analysis
    sentiment_report = perform_sentiment_analysis(reviews)

    return render_template('index.html', report=sentiment_report)



if __name__ == '__main__':
    app.run(debug=True)
