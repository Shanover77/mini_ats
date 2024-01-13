from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    TokenClassificationPipeline
)
from transformers.pipelines import AggregationStrategy
import numpy as np
import nltk
import re

# Download NLTK stopwords data
# nltk.download('stopwords')

# Import NLTK stopwords
from nltk.corpus import stopwords

# Define keyphrase extraction pipeline
class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model, *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model),
            tokenizer=AutoTokenizer.from_pretrained(model),
            *args,
            **kwargs
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return np.unique([result.get("word").strip() for result in results])

def extract_skills(text):
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word.lower() not in stop_words])

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    model_name = "ml6team/keyphrase-extraction-kbir-inspec"
    extractor = KeyphraseExtractionPipeline(model=model_name)
    keyphrases = extractor(text)
    return keyphrases

