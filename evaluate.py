import pandas as pd
import spacy

# Load your trained spaCy model
nlp = spacy.load("/model")

# Function to classify text using your model
def classify_text(text):
    doc = nlp(text)
    # Assuming your model outputs a 'cats' dictionary with 'FAKE' and 'REAL' probabilities
    # Adjust this according to your model's output
    if doc.cats['REAL'] > doc.cats['FAKE']:
        prediction = 1
    else:
        prediction = 0

    return prediction

# Load your dataset
df = pd.read_csv('test_data_classifier.csv', header=None, names=['text', 'isReal', 'Prediction'])

# Apply the classification function to each article
df['Prediction'] = df['text'].apply(classify_text)

df['isReal'] = pd.to_numeric(df['isReal'], errors='coerce')
# Assuming your Prediction column is already of integer type after the classify_text function

print(df.head())  # To check the first few rows for sanity
print(df.dtypes)  # To verify the data types of your columns

# Calculate accuracy
accuracy = (df['isReal'] == df['Prediction']).mean()
print(f"Accuracy: {accuracy:.4f}")

# Optional: Save the dataframe with predictions to a new CSV file
df.to_csv('classifier_results.csv', index=False)
