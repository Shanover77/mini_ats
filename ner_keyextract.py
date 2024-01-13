from transformers import pipeline

# Load the NER pipeline with a pre-trained BERT model
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Example job description
job_description = "We are looking for a software engineer with expertise in Python, Java, and machine learning."

# Use the NER pipeline to extract entities
results = ner_pipeline(job_description)

# Print all entities and their labels
for entity in results:
    print(f"Entity: {entity['word']}, Label: {entity['entity']}")
