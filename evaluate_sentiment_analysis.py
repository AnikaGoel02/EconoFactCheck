import pandas as pd
import spacy

# Load your trained spaCy model
nlp = spacy.load("/sentAnalysisModel")

# Function to classify text using your model
def classify_text(text):
    doc = nlp(text)
    my_dict = doc.cats
    key_of_highest_value = max(my_dict, key=my_dict.get)

    if key_of_highest_value == 'POSITIVE':
        prediction = 'positive'
    elif key_of_highest_value == 'NEGATIVE':
        prediction = 'negative'
    else:
        prediction = 'neutral'

    return prediction

# Load your dataset
df = pd.read_csv('sentiment_analysis_test.csv', header=None, names=['text', 'sentiment', 'prediction'])

# Apply the classification function to each article
df['prediction'] = df['text'].apply(classify_text)

# df['isReal'] = pd.to_numeric(df['isReal'], errors='coerce')
# Assuming your Prediction column is already of integer type after the classify_text function

# print(df.head())  # To check the first few rows for sanity
# print(df.dtypes)  # To verify the data types of your columns


# Optional: Save the dataframe with predictions to a new CSV file
df.to_csv('sentAnalysis_eval_results.csv', index=False)
