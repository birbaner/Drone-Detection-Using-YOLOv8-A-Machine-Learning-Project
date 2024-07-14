import streamlit as st
from transformers import pipeline

# Title of the app
st.title("Sentiment Analysis App") #Sets the title of the Streamlit app to "Sentiment Analysis App".

# Input text from the user
user_input = st.text_area("Enter text to analyze") #Creates a text area where users can input the text they want to analyze.

# Select pretrained model
#distilbert-base-uncased-finetuned-sst-2-english: A DistilBERT model fine-tuned for sentiment analysis on the SST-2 dataset.
#nlptown/bert-base-multilingual-uncased-sentiment: A BERT model trained for sentiment analysis on multiple languages.

model_name = st.selectbox("Select a pretrained model", ["distilbert-base-uncased-finetuned-sst-2-english", "nlptown/bert-base-multilingual-uncased-sentiment"]) #Provides a dropdown menu for users to select a pretrained model provided by the HuggingFace Transformers library

# Initialize the sentiment analysis pipeline
sentiment_analysis = pipeline("sentiment-analysis", model=model_name,device=-1) #Initializes the sentiment analysis pipeline using the selected model.

# Perform sentiment analysis when the button is clicked
if st.button("Analyze"): #reates a button labeled "Analyze". When clicked, it triggers the sentiment analysis.
    if user_input:
        results = sentiment_analysis(user_input) #If text is entered, the sentiment analysis pipeline processes the text
        st.write(results) #results are displayed 
    else:
        st.write("Please enter some text to analyze") #If no text is entered, a message prompting the user to enter some text is displayed
