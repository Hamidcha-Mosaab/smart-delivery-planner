from textblob import TextBlob
def simple_sentiment(text):
    if not text:
        return {"label":"neutral","score":0.0}
    s = TextBlob(text).sentiment.polarity
    if s > 0.1: return {"label":"positive","score":s}
    if s < -0.1: return {"label":"negative","score":s}
    return {"label":"neutral","score":s}
