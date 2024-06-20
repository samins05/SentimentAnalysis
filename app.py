from textblob import TextBlob

text_1 = "The pizza was quite bland. It could use a bit more seasoning."
p_1 = TextBlob(text_1).sentiment.polarity
print("Polarity of Text 1 is", p_1)

'''from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")
data = ["This pizza was okay."]
print(sentiment_pipeline(data))
'''