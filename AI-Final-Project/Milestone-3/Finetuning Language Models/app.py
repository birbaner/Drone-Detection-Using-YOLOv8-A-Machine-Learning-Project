import streamlit as st
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from datasets import load_dataset

# Load model and tokenizer
model_path = "rb757/new_app"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load the dataset
dataset_dict = load_dataset(
    'HUPD/hupd',
    name='sample',
    data_files="https://huggingface.co/datasets/HUPD/hupd/resolve/main/hupd_metadata_2022-02-22.feather",
    train_filing_start_date='2016-01-01',
    train_filing_end_date='2016-01-21',
    val_filing_start_date='2016-01-22',
    val_filing_end_date='2016-01-31',
    trust_remote_code=True
)

# Convert to DataFrame
train_df = pd.DataFrame(dataset_dict['train'])
val_df = pd.DataFrame(dataset_dict['validation'])

# Print columns to verify availability
print("Train set columns:", train_df.columns.tolist())
print("Validation set columns:", val_df.columns.tolist())

# Check if 'patent_number' exists
if 'patent_number' not in train_df.columns:
    st.error("Column 'patent_number' not found in the training dataset.")
else:
    # Title and description
    st.title("📜 Milestone Patent Evaluation")
    st.write("Select a patent application to evaluate its patentability.")

    # Dropdown for patent numbers
    patent_numbers = train_df['patent_number'].unique()
    selected_patent = st.selectbox("Select Patent Number", patent_numbers)

    # Retrieve relevant information
    patent_info = train_df[train_df['patent_number'] == selected_patent].iloc[0]
    title = patent_info['title']
    abstract = patent_info['abstract']
    claims = patent_info['claims']
    background = patent_info['background']
    summary = patent_info['summary']
    description = patent_info['description']
    cpc_label = patent_info['cpc_label']
    ipc_label = patent_info['ipc_label']
    filing_date = patent_info['filing_date']
    patent_issue_date = patent_info['patent_issue_date']
    date_published = patent_info['date_published']
    examiner_id = patent_info['examiner_id']

    # Display the information
    st.markdown("### Title")
    st.markdown(f"**{title}**")
    
    st.markdown("---")
    
    st.markdown("### Abstract")
    st.text_area("Abstract", abstract, height=150)
    
    st.markdown("---")
    
    st.markdown("### Claims")
    st.text_area("Claims", claims, height=150)
    
    st.markdown("---")
    
    st.markdown("### Background")
    st.text_area("Background", background, height=150)
    
    st.markdown("---")
    
    st.markdown("### Summary")
    st.text_area("Summary", summary, height=150)
    
    st.markdown("---")
    
    st.markdown("### Description")
    st.text_area("Description", description, height=150)
    
    st.markdown("---")
    
    st.markdown("### CPC Label")
    st.markdown(f"**{cpc_label}**")
    
    st.markdown("### IPC Label")
    st.markdown(f"**{ipc_label}**")
    
    st.markdown("### Filing Date")
    st.markdown(f"**{filing_date}**")
    
    st.markdown("### Patent Issue Date")
    st.markdown(f"**{patent_issue_date}**")
    
    st.markdown("### Date Published")
    st.markdown(f"**{date_published}**")
    
    st.markdown("### Examiner ID")
    st.markdown(f"**{examiner_id}**")

    # Submit button
    if st.button("Get Patentability Score"):
        # Prepare the input text
        input_text = f"{title} {abstract} {claims} {background} {summary} {description}"
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)

        # Get the model prediction
        with torch.no_grad():
            logits = model(**inputs).logits
            predictions = torch.argmax(logits, dim=-1)

        # Display the patentability score
        decision_labels = ['REJECTED', 'ACCEPTED', 'PENDING', 'CONT-REJECTED', 'CONT-ACCEPTED', 'CONT-PENDING']
        score = decision_labels[predictions.item()]
        st.success(f"Patentability Score: **{score}**")
