import io
import fitz  # PyMuPDF
from docx import Document
import streamlit as st
import spacy
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def show_wordcloud(data):
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='Blues',  # You can change the color map to any you prefer
        collocations=False  # This is to ensure the same words are not counted multiple times
    ).generate(data)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    st.pyplot(fig)


# Function to plot pie chart
def plot_sentiment_pie_chart(sentiments):
    labels = sentiments.keys()
    sizes = sentiments.values()
    colors = ['lightgreen', 'lightcoral', 'lightblue']  # Custom colors for Positive, Negative, Neutral
    explode = (0.1, 0, 0)  # explode the 1st slice (Positive)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig1


def analyze_sentiment(input_text):
    nlp = spacy.load("/sentAnalysisModel")
    doc = nlp(input_text)
    # Assuming your model has sentiment analysis capabilities
    # This part might change based on how your model provides sentiment scores
    sentiment = doc.cats if hasattr(doc, 'cats') else "Sentiment analysis not supported"
    return sentiment


def read_pdf(uploaded_file):
    # Convert the uploaded file to a bytes stream
    bytes_stream = io.BytesIO(uploaded_file.getvalue())
    # Open the PDF with fitz
    pdf = fitz.open("pdf", bytes_stream)
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

def read_docx(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def read_text_file(file):
    # Assuming the file is in UTF-8 -- adjust encoding as necessary
    text = file.getvalue().decode("utf-8")
    return text

def fetch_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # This is a simplistic approach; you might need to adjust the logic
        # to target specific tags or classes depending on the website's structure.
        article_text = ' '.join([p.text for p in soup.find_all('p')])
        return article_text
    else:
        return "Failed to fetch the article."

# Function to classify the article (placeholder function)
def classify_article(input_text):
    # Loading the trained model
    nlp = spacy.load("/model")

    doc = nlp(input_text)

    return doc.cats


def get_highest_value(result_dict):
    return max(result_dict, key=result_dict.get)


# Set up the main structure of the app
def main():
    st.title("EconoFactCheck")
    st.write("Welcome to EconoFactCheck, a fake financial news detector. Select your input type and submit an article for detection.")

    # Radio button to select input type
    input_type = st.radio("Choose the input type:", ('URL', 'Text', 'Local Directory'))

    # Conditional input field based on the input type selected
    if input_type == 'URL':
        article_url = st.text_input("Enter the URL of the article:")
        if article_url:
            article_input = fetch_article_content(article_url)
        else:
            st.write("Please enter a URL.")
        if st.button("Fetch Article"):
            st.text_area("Article text:", value=article_input, height=200)
    elif input_type == 'Text':
        article_input = st.text_area("Enter the article text:")
    else:
        # Using file_uploader to select a file from the directory
        # Note: Streamlit does not directly support browsing directories, so this is a workaround
        file = st.file_uploader("Choose a file from the directory you want to examine", accept_multiple_files=False)
        if file is not None:
            # Check the file type and process accordingly
            if file.type == "application/pdf":
                article_input = read_pdf(file)
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                article_input = read_docx(file)
            elif file.type == "text/plain":
                article_input = read_text_file(file)
            else:
                st.error("Unsupported file type")

    if st.button("Classify Article"):
        if article_input:
            # Classify the article
            result = classify_article(article_input)
            sentiment_result = analyze_sentiment(article_input)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Classification")
                st.write(f"The article is classified as: {get_highest_value(result)}")

            with col2:
                st.subheader("Sentiment Analysis")
                st.write(f"Sentiment analysis result: {get_highest_value(sentiment_result)}")

            with st.expander("Details"):
                st.write(f"Classification details: {result}")
                st.write(f"Sentiment analysis details: {sentiment_result}")

    if st.button("Show Visualizations"):
        if article_input:
            vis_col1, vis_col2 = st.columns(2)
            with vis_col1:
                st.subheader("WordCloud")
                show_wordcloud(article_input)

            with vis_col2:
                st.subheader("Sentiment Pie Chart")
                sentiment_result = analyze_sentiment(article_input)
                fig = plot_sentiment_pie_chart(sentiment_result)
                st.pyplot(fig)
        else:
            st.write("Please enter an article.")


if __name__ == "__main__":
    main()
