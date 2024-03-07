"""
__author__ = "Anika Goel"
__version__ = "1.0.1"
__maintainer__ = "Anika Goel"
__status__ = "Prototype"
"""

import spacy
from spacy.util import minibatch, compounding
import random
from spacy.training.example import Example
import logging
from spacy.pipeline.textcat import Config, single_label_cnn_config
import os
import pandas as pd

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def clean_data(data):
    # Drop rows where 'text' column has NaN values
    data.dropna(subset=['text'], inplace=True)

    # Optionally, you might also want to reset the index after dropping rows
    data.reset_index(drop=True, inplace=True)

    # Now, your dataset 'data' will only contain rows where the 'text' column has valid text entries
    return data

def fine_tune(df):
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Add text classifier to the pipeline
    textcat = nlp.add_pipe("textcat", last=True)
    textcat.add_label("FAKE")
    textcat.add_label("REAL")

    # Prepare training data (assuming your DataFrame is named 'df')
    train_texts = df['text'].values
    train_labels = [{'cats': {'FAKE': label == 0, 'REAL': label == 1}} for label in df['isReal']]

    train_data = list(zip(train_texts, train_labels))

    # Train the model
    random.seed(1)
    spacy.util.fix_random_seed(1)
    optimizer = nlp.begin_training()

    for epoch in range(10):
        random.shuffle(train_data)
        losses = {}
        batches = minibatch(train_data, size=compounding(4., 32., 1.001))
        batch_number = 0

        for batch in batches:
            texts, annotations = zip(*batch)
            examples = [Example.from_dict(nlp.make_doc(text), ann) for text, ann in zip(texts, annotations)]
            nlp.update(examples, drop=0.5, sgd=optimizer, losses=losses)
            batch_number += 1

            # Log the progress for each batch
            logging.info(f"Epoch {epoch}, Batch {batch_number}, Loss: {losses}")

        # Log the losses at the end of each epoch
        logging.info(f"Losses at end of epoch {epoch}: {losses}")

    # Save the trained model
    nlp.to_disk("/model")


def classify_text(text):
    # Loading the trained model
    nlp = spacy.load("../model")

    doc = nlp(text)

    return doc

def supportSentimentAnalysis():
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Load the training data
    df = pd.read_csv('sample_train_sentAnalysis.csv')

    # Add text classifier to the pipeline
    textcat = nlp.add_pipe("textcat", last=True)
    textcat.add_label("POSITIVE")
    textcat.add_label("NEGATIVE")
    textcat.add_label("NEUTRAL")

    # Prepare training data (assuming your DataFrame is named 'df')
    train_texts = df['text'].values
    train_labels = [{'cats': {'POSITIVE': label == 'positive', 'NEGATIVE': label == 'negative',
                              'NEUTRAL': label == 'neutral'}} for label in df['sentiment']]

    train_data = list(zip(train_texts, train_labels))

    # Train the model
    random.seed(1)
    spacy.util.fix_random_seed(1)
    optimizer = nlp.begin_training()

    for epoch in range(10):
        random.shuffle(train_data)
        losses = {}
        batches = minibatch(train_data, size=compounding(4., 32., 1.001))
        batch_number = 0

        for batch in batches:
            texts, annotations = zip(*batch)
            examples = [Example.from_dict(nlp.make_doc(text), ann) for text, ann in zip(texts, annotations)]
            nlp.update(examples, drop=0.5, sgd=optimizer, losses=losses)
            batch_number += 1

            # Log the progress for each batch
            logging.info(f"Epoch {epoch}, Batch {batch_number}, Loss: {losses}")

        # Log the losses at the end of each epoch
        logging.info(f"Losses at end of epoch {epoch}: {losses}")

    # Save the trained model
    nlp.to_disk("/sentAnalysisModel")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Reading data from a CSV file into a DataFrame
    # original_df = pd.read_csv('sample_data.csv')

    # Cleaning the Dataset
    # df = clean_data(original_df)

    # Training the model
    # fine_tune(df)

    # supportSentimentAnalysis()
    # Loading the trained model
    nlp = spacy.load("/sentAnalysisModel")
    # nlp = spacy.load("/model")
    # # Process text
    # doc = nlp("This is some text to process.")
    #
    # # Do something with the doc, e.g., print text classifications
    # print(doc.cats)
    # test_text = "BUENOS AIRES (Reuters) - Argentine leader Mauricio Macri said Wednesdayâ€™s state visit by U.S. President Barack Obama marked the start of new â€œmatureâ€  relations in which the countries would cooperate on issues ranging from trade to fighting international drug trafficking. "
    test_text = "MONTCLAIR, NJ—Saying that a lot had changed since Old St. Nick left the North Pole last Christmas, a local mall Santa instructed children Monday not to sit on Santa’s colostomy bag. “Ho, ho, ho, Santa is so excited to see all his favorite boys and girls, so long as they are very careful when they come to say hello,” said the jolly, bearded Kris Kringle, who then pointed to a small, gift-wrapped pouch on his leg and added that anyone who sat on Santa’s special present would be put on the naughty list this year. “Why, hello, young man, you’ve been very good this year, haven’t you? Now, let’s move to the other leg and stop punching Santa’s tummy. We don’t want Santa to get a deadly infection, and die right here on Candy Cane Lane, do we? Ho, ho, ho! Seriously, can someone get this kid off of me?” At press time, several elves were spotted rushing Santa to the bathroom after a particularly large boy had sat on Santa’s lap, kicked Santa in the groin, and burst the colostomy bag."
    doc = nlp(test_text)
    print("Output:", doc.cats)
