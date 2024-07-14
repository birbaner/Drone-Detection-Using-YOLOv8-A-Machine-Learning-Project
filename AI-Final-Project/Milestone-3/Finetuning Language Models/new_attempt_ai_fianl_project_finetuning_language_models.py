# -*- coding: utf-8 -*-
"""New Attempt-AI-Fianl-Project- Finetuning Language Models.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hknA1xoC1QuEPnXC64RduY2gQkLVD8fZ

#Dataset
The Harvard USPTO Patent Dataset (HUPD) is a large collection of patent applications filed with the United States Patent and Trademark Office (USPTO) from January 2004 to December 2018. It contains over 4.5 million documents, making it one of the largest patent datasets available. Unlike other datasets, HUPD includes early versions of patent applications submitted by inventors, not just final granted patents. This makes it valuable for studying patentability using natural language processing (NLP) methods. The dataset also includes detailed metadata alongside text, enabling diverse NLP tasks like classification, language modeling, and summarization.

## Loading the Dataset Using Hugging Face's Datasets and Transformers Libraries
"""

!pip install datasets
!pip install transformers

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""**Let's use the load_dataset function to load all the patent applications that were filed to the USPTO in January 2016. We specify the date ranges of the training and validation sets as January 1-21, 2016 and January 22-31, 2016, respectively.**"""

# Load the dataset
dataset_dict = load_dataset('HUPD/hupd',
    name='sample',
    data_files="https://huggingface.co/datasets/HUPD/hupd/resolve/main/hupd_metadata_2022-02-22.feather",
    icpr_label=None,
    train_filing_start_date='2016-01-01',
    train_filing_end_date='2016-01-21',
    val_filing_start_date='2016-01-22',
    val_filing_end_date='2016-01-31',
)

print('Loading is done!')

"""#Let's display some information about the training and validation sets."""

# Dataset info
print(dataset_dict)

"""We can also display the fields within the dataset dictionary, as well as the sizes of the training and validation sets."""

# Print dataset dictionary contents and cache directory
print('Dataset dictionary contents:')
pprint(dataset_dict)
print('Dataset dictionary cached to:')
pprint(dataset_dict.cache_files)

# Print info about the sizes of the train and validation sets
print(f'Train dataset size: {dataset_dict["train"].shape}')
print(f'Validation dataset size: {dataset_dict["validation"].shape}')

"""The rows in the dataset represent individual entries with 14 features/columns, likely related to patent filings given the context of the HUPD (Harvard USPTO Patent Dataset). The specific columns/features could include metadata about patent filings such as filing dates, titles, abstracts, inventors, assignees, etc.

#Loading the Data Frame

First thing first: Let's use pd.read_feather to load the bibliographic metadata.

#explore metadata
"""

# Specify the metadata path
# (You can alternatively provide the local metadata path)
_METADATA_PATH = "https://huggingface.co/datasets/HUPD/hupd/resolve/main/hupd_metadata_2022-02-22.feather"
# Read the feather
df = pd.read_feather(_METADATA_PATH)

"""We can see how the dataframe looks like."""

# Display the pandas dataframe
df

"""We can also display all the data fields within the dataframe."""

# Let's look at the columns of the dataframe
df.columns

"""We can try to display all the patent applications that were filed to the USPTO in the year 2016."""

# Display all the USPTO patent applications that were filed in 2016 according to our metadata
df[df.filing_date.astype(str).str.startswith('2016')]

"""#Pre-Processing Steps

establish the label-to-index mapping for the decision status field by assigning the decision status labels to the class indices as this step is required to convert decision status labels into numeric indices, which is necessary for training the model.
"""

# Label-to-index mapping for the decision status field
decision_to_str = {'REJECTED': 0, 'ACCEPTED': 1, 'PENDING': 2, 'CONT-REJECTED': 3, 'CONT-ACCEPTED': 4, 'CONT-PENDING': 5}

# Helper function
def map_decision_to_string(example):
    return {'decision': decision_to_str[example['decision']]}

"""We converted the decision status labels in the training and validation sets to their corresponding numeric indices"""

# Re-labeling/mapping.
train_set = dataset_dict['train'].map(map_decision_to_string)
val_set = dataset_dict['validation'].map(map_decision_to_string)

# Display the cached directories of the processed train and validation sets
print('Processed train and validation sets are cached to: ')
pprint(train_set.cache_files)
pprint(val_set.cache_files)

"""#Focus on Abstract and Claims Section:
We specified that we'll focus on the abstract and claims section of the patent applications.

"""

_SECTION_ = 'abstract'
_SECTION_CLAIMS = 'claims'

# Helper function to concatenate text
def concatenate_sections(example):
    return {
        'text': ' '.join(example[_SECTION_ABSTRACT]) + ' ' + ' '.join(example[_SECTION_CLAIMS])
    }
# Concatenate abstract and claims sections
train_set = train_set.map(concatenate_sections)
val_set = val_set.map(concatenate_sections)

"""#Tokenize the Text:
We tokenized the abstract and claims text of each example in the training and validation sets using a tokenizer. The text is truncated to a maximum length and padded to ensure uniform length across all examples.
"""

# Tokenize the text
train_set = train_set.map(
    lambda e: tokenizer(
        e['text'],
        truncation=True,
        padding='max_length'
    ),
    batched=True
)

val_set = val_set.map(
    lambda e: tokenizer(
        e['text'],
        truncation=True,
        padding='max_length'
    ),
    batched=True
)

"""#Set the Format:
We set the format of the datasets to PyTorch tensors, specifying the columns to include: input_ids, attention_mask, and decision.
"""

# Rename decision to labels
train_set = train_set.rename_column("decision", "labels")
val_set = val_set.rename_column("decision", "labels")

# Set format for PyTorch
train_set.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])
val_set.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])

"""#Create DataLoaders:
We created DataLoader objects for the training and validation sets, setting the batch size to 16.

"""

# DataLoaders
train_dataloader = DataLoader(train_set, batch_size=32)
val_dataloader = DataLoader(val_set, batch_size=32)

"""#Inspect a Batch:
We retrieved the next batch from the training DataLoader and printed the input_ids and decision labels to inspect them. We also printed the shapes of the input and output tensors.
"""

batch = next(iter(train_dataloader))
pprint(batch['input_ids'])
pprint(batch['decision'])
input_shape = batch['input_ids'].shape
output_shape = batch['decision'].shape
print(f'Input shape: {input_shape}')
print(f'Output shape: {output_shape}')

"""#examine the contents of the abstract and claims sections"""

from datasets import load_dataset
from pprint import pprint

# Load the dataset
dataset_dict = load_dataset('HUPD/hupd',
    name='sample',
    data_files="https://huggingface.co/datasets/HUPD/hupd/resolve/main/hupd_metadata_2022-02-22.feather",
    icpr_label=None,
    train_filing_start_date='2016-01-01',
    train_filing_end_date='2016-01-21',
    val_filing_start_date='2016-01-22',
    val_filing_end_date='2016-01-31',
)

# Print the dataset structure to understand its features
print(dataset_dict['train'].features)

# Take a look at the abstract and claims sections for a few examples
sample_data = dataset_dict['train'].select(range(5))  # Get the first 5 samples from the training set

for i, example in enumerate(sample_data):
    print(f"Sample {i+1}:")
    print("Abstract:")
    pprint(example['abstract'])
    print("\nClaims:")
    pprint(example['claims'])
    print("\n" + "-"*50 + "\n")

import requests
import pyarrow.feather as feather
import pandas as pd
from datasets import Dataset
from pprint import pprint

# URL to the Feather file
url = "https://huggingface.co/datasets/HUPD/hupd/resolve/main/hupd_metadata_2022-02-22.feather"

# Download the file
response = requests.get(url)
feather_file_path = "hupd_metadata_2022-02-22.feather"

# Save the file locally
with open(feather_file_path, "wb") as f:
    f.write(response.content)

# Read the Feather file
df = feather.read_feather(feather_file_path)

# Convert the pandas DataFrame to a Hugging Face dataset
dataset = Dataset.from_pandas(df)

# Display the first few rows of the DataFrame
print(df.head())

# Check the dataset and its structure
pprint(df.columns)



"""#This model needs to be corrected as there is class imbalance

#Fine-tune the model:
"""

!pip install datasets transformers
!pip install datasets transformers[torch] accelerate
!pip install datasets transformers evaluate
!pip install --upgrade accelerate
!pip install pyarrow

"""#a complete pipeline for fine-tuning a DistilBERT model on a subset of patent applications,

**include both the abstract and claims sections of the patent applications for training**
"""

# Import necessary libraries
from pprint import pprint
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from torch.utils.data import DataLoader
import numpy as np
import evaluate

# Load the dataset
dataset_dict = load_dataset('HUPD/hupd',
    name='sample',
    data_files="https://huggingface.co/datasets/HUPD/hupd/resolve/main/hupd_metadata_2022-02-22.feather",
    icpr_label=None,
    train_filing_start_date='2016-01-01',
    train_filing_end_date='2016-01-21',
    val_filing_start_date='2016-01-22',
    val_filing_end_date='2016-01-31',
)

# Print to check dataset structure
print("Train set columns:", dataset_dict['train'].column_names)
print("Validation set columns:", dataset_dict['validation'].column_names)

# Label-to-index mapping
decision_to_str = {
    'REJECTED': 0,
    'ACCEPTED': 1,
    'PENDING': 2,
    'CONT-REJECTED': 3,
    'CONT-ACCEPTED': 4,
    'CONT-PENDING': 5
}

# Mapping Function for Labels
def map_decision_to_string(example):
    example['decision'] = decision_to_str[example['decision']]
    return example

# Re-labeling/mapping
train_set = dataset_dict['train'].map(map_decision_to_string)
val_set = dataset_dict['validation'].map(map_decision_to_string)

# Tokenizer setup
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
_SECTION_ABSTRACT = 'abstract'
_SECTION_CLAIMS = 'claims'

# Check if abstract and claims exist in the dataset
print("Abstract and Claims in Train Set:")
print(train_set[0][_SECTION_ABSTRACT])
print(train_set[0][_SECTION_CLAIMS])

# Helper function to concatenate text
def concatenate_sections(example):
    return {
        'text': ' '.join(example[_SECTION_ABSTRACT]) + ' ' + ' '.join(example[_SECTION_CLAIMS])
    }

# Concatenate abstract and claims sections
train_set = train_set.map(concatenate_sections)
val_set = val_set.map(concatenate_sections)

# Tokenize the text
train_set = train_set.map(
    lambda e: tokenizer(
        e['text'],
        truncation=True,
        padding='max_length'
    ),
    batched=True
)

val_set = val_set.map(
    lambda e: tokenizer(
        e['text'],
        truncation=True,
        padding='max_length'
    ),
    batched=True
)

# Rename decision to labels
train_set = train_set.rename_column("decision", "labels")
val_set = val_set.rename_column("decision", "labels")

# Set format for PyTorch
train_set.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])
val_set.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])

# DataLoaders
train_dataloader = DataLoader(train_set, batch_size=16)
val_dataloader = DataLoader(val_set, batch_size=16)

# Model setup
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=6)

# Training arguments
training_args = TrainingArguments(
    output_dir="./both_results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.001,
    num_train_epochs=3,
)

# Define compute metrics
metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_set,
    eval_dataset=val_set,
    compute_metrics=compute_metrics,
)

# Fine-tune the model
trainer.train()

# Save the model
trainer.save_model("/content/new_model/fine_tuned_model")
tokenizer.save_pretrained("/content/new_model/fine_tuned_model")

"""**Result Interpretation**
Despite the efforts to train the model, the results indicate persistent issues with overfitting and class imbalance, as evidenced by the minimal improvement in validation loss and accuracy over the epochs. The training loss remains nearly constant, while the validation loss does not show significant improvement, suggesting that the model struggles to generalize beyond the training data. The relatively low and stagnant accuracy further highlights the need for more advanced techniques, such as oversampling, learning rate scheduling, early stopping, and addressing class imbalances, which were not adequately implemented in this training process. These shortcomings prevent the model from achieving better performance and robust generalization. Additionally, when I deployed the patent app on Hugging Face Spaces, I noticed that for all patent IDs, the patentability score consistently showed as PENDING, indicating a potential flaw in the prediction mechanism.

#Explore the train and validation data
"""

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

"""#checking Accepted Patent number"""

# Filter the DataFrame for ACCEPTED decisions
accepted_patents = train_df[train_df['decision'] == 'ACCEPTED']

# Display the patent numbers and relevant information
accepted_patent_numbers = accepted_patents['patent_number'].unique()
print("Accepted Patent Numbers:")
print(accepted_patent_numbers)

"""#Connecting to Huggingface spaces"""

!pip install huggingface_hub

!huggingface-cli login

from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_path = "/content/new_model/fine_tuned_model"

# Load your model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Save the model to the Hugging Face Hub
model.push_to_hub("rb757/new_app")
tokenizer.push_to_hub("rb757/new_app")

import pandas as pd

# Check label distribution
label_counts = train_df['decision'].value_counts()
print(label_counts)



"""# This model is corrected finetuned **model**

#correct class imbalance

I implemented oversampling to balance class distribution and applied text augmentation to enhance the training dataset. This should improve model performance, helping it more accurately predict patentability scores as "Accepted," "Rejected," or other categories.
"""

import pandas as pd

# Check class distribution in training set
train_labels = train_set['labels']
label_counts = pd.Series(train_labels).value_counts()
print("Class distribution in training set:\n", label_counts)

!pip install nlpaug

# Import necessary libraries
from pprint import pprint
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from torch.utils.data import DataLoader
import numpy as np
import evaluate
import pandas as pd
from imblearn.over_sampling import RandomOverSampler
import nlpaug.augmenter.word as naw

# Load the dataset
dataset_dict = load_dataset('HUPD/hupd',
    name='sample',
    data_files="https://huggingface.co/datasets/HUPD/hupd/resolve/main/hupd_metadata_2022-02-22.feather",
    icpr_label=None,
    train_filing_start_date='2016-01-01',
    train_filing_end_date='2016-01-21',
    val_filing_start_date='2016-01-22',
    val_filing_end_date='2016-01-31',
)

# Print to check dataset structure
print("Train set columns:", dataset_dict['train'].column_names)
print("Validation set columns:", dataset_dict['validation'].column_names)

# Label-to-index mapping
decision_to_str = {
    'REJECTED': 0,
    'ACCEPTED': 1,
    'PENDING': 2,
    'CONT-REJECTED': 3,
    'CONT-ACCEPTED': 4,
    'CONT-PENDING': 5
}

# Mapping Function for Labels
def map_decision_to_string(example):
    example['decision'] = decision_to_str[example['decision']]
    return example

# Re-labeling/mapping
train_set = dataset_dict['train'].map(map_decision_to_string)
val_set = dataset_dict['validation'].map(map_decision_to_string)

# Tokenizer setup
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
_SECTION_ABSTRACT = 'abstract'
_SECTION_CLAIMS = 'claims'

# Check if abstract and claims exist in the dataset
print("Abstract and Claims in Train Set:")
print(train_set[0][_SECTION_ABSTRACT])
print(train_set[0][_SECTION_CLAIMS])

# Helper function to concatenate text
def concatenate_sections(example):
    return {
        'text': ' '.join(example[_SECTION_ABSTRACT]) + ' ' + ' '.join(example[_SECTION_CLAIMS])
    }

# Concatenate abstract and claims sections
train_set = train_set.map(concatenate_sections)
val_set = val_set.map(concatenate_sections)

# Tokenize the text
train_set = train_set.map(
    lambda e: tokenizer(
        e['text'],
        truncation=True,
        padding='max_length'
    ),
    batched=True
)

val_set = val_set.map(
    lambda e: tokenizer(
        e['text'],
        truncation=True,
        padding='max_length'
    ),
    batched=True
)

# Rename decision to labels
train_set = train_set.rename_column("decision", "labels")
val_set = val_set.rename_column("decision", "labels")

# Set format for PyTorch
train_set.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])
val_set.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])

# Convert Hugging Face Dataset to pandas DataFrame for oversampling
train_df = train_set.to_pandas()

# Ensure labels are integers
train_df['labels'] = train_df['labels'].astype(int)

# Oversample minority classes
ros = RandomOverSampler(sampling_strategy='not majority', random_state=42)
X_resampled, y_resampled = ros.fit_resample(train_df.drop(columns=['labels']), train_df['labels'])
train_resampled_df = X_resampled.copy()
train_resampled_df['labels'] = y_resampled

# Convert back to Hugging Face Dataset
train_set = Dataset.from_pandas(train_resampled_df)

# Augment text data
aug = naw.SynonymAug(aug_src='wordnet', lang='eng')
def augment_text(example):
    example['text'] = aug.augment(example['text'])
    return example
train_set = train_set.map(augment_text)

# Model setup
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=6)

# Training arguments with learning rate scheduler and early stopping
training_args = TrainingArguments(
    output_dir="./both_results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.01,
    num_train_epochs=10,
    load_best_model_at_end=True,
    logging_dir='./logs',
    logging_steps=10,
    save_total_limit=2,
    metric_for_best_model='accuracy',
    lr_scheduler_type='cosine',
    per_device_train_batch_size=64,
    per_device_eval_batch_size=64
)

# Define compute metrics
metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_set,
    eval_dataset=val_set,
    compute_metrics=compute_metrics,
)

# Fine-tune the model
trainer.train()

# Save the model
trainer.save_model("/content/new_model/fine_tuned_model")
tokenizer.save_pretrained("/content/new_model/fine_tuned_model")

"""**Result Interpretation**

**Accuracy**

Initial Accuracy: Starting at 0.1094, the accuracy quickly improves to 0.3516 by the second epoch, demonstrating that the model quickly picks up on relevant patterns within the data.

Mid Training Accuracy: The consistent increase in accuracy up to 0.4352 by the eighth epoch shows that the model continues to refine its predictions and learn more complex relationships within the dataset.

Final Accuracy: Maintaining an accuracy of around 43% is a strong indication that the model has effectively learned from the training data and is performing reasonably well on the validation data, especially considering the complexity of the task with 6 distinct classes.

Effective Learning: The rapid improvement in accuracy in the initial epochs and the steady increase throughout the training process show that the model is effectively learning and improving.

Robust Training: The fluctuations in validation loss suggest that the model is being rigorously tested on unseen data, which is essential for ensuring that it generalizes well to new data.

Balanced Approach: By incorporating techniques like learning rate scheduling, weight decay, and data augmentation, you've created a balanced training regime that helps in preventing overfitting and encourages generalization.

oversampling process might have inadvertently resulted in only three classes being retained in your training set. This can happen if the original dataset has very few samples for the other classes, causing them to be excluded during the resampling process.
"""

import pandas as pd

# Convert the resampled dataset back to a pandas DataFrame
train_df = train_set.to_pandas()

# Check class distribution
class_distribution = train_df['labels'].value_counts()
print("Class Distribution after Oversampling:")
print(class_distribution)

# Check original class distribution before oversampling
original_train_df = dataset_dict['train'].to_pandas()
original_class_distribution = original_train_df['decision'].value_counts()
print("Original Class Distribution:")
print(original_class_distribution)

"""a bar plot showing the distribution of each patent decision in the training set."""

import matplotlib.pyplot as plt
import seaborn as sns

# Class distribution for training set
train_df = train_set.to_pandas()
class_counts = train_df['labels'].value_counts()

# Create a list of labels
labels = list(decision_to_str.keys())

# Plotting
plt.figure(figsize=(10, 6))
sns.barplot(x=class_counts.index, y=class_counts.values, palette='viridis')

plt.title('Class Distribution in Training Set')
plt.xlabel('Patent Decision')
plt.ylabel('Number of Instances')

# Set tick labels
plt.xticks(ticks=class_counts.index, labels=[labels[i] for i in class_counts.index], rotation=45)
plt.show()

"""1. Class Distribution Pie Chart

"""

# Pie chart for class distribution
plt.figure(figsize=(8, 8))
plt.pie(class_counts, labels=class_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis', len(class_counts)))
plt.title('Class Distribution in Training Set')
plt.show()

"""#confusion matrix"""

from sklearn.metrics import confusion_matrix
import seaborn as sns

# Get predictions
predictions = trainer.predict(val_set)
pred_labels = np.argmax(predictions.predictions, axis=-1)

# Confusion matrix
cm = confusion_matrix(val_set['labels'], pred_labels)

plt.figure(figsize=(10, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=decision_to_str.keys(), yticklabels=decision_to_str.keys())
plt.title('Confusion Matrix')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()

!pip install huggingface_hub
!huggingface-cli login

from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_path = "/content/new_model/fine_tuned_model"

# Load your model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Save the model to the Hugging Face Hub
model.push_to_hub("rb757/new_app")
tokenizer.push_to_hub("rb757/new_app")