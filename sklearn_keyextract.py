from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import LatentDirichletAllocation

def extract_keywords(text, num_keywords=5):
    """
    Extract and return main keywords from the given text using machine learning models.

    Parameters:
    - text (str): The input text from which keywords need to be extracted.
    - num_keywords (int): The number of keywords to extract (default is 5).

    Returns:
    - List[str]: A list of main keywords extracted from the input text.
    """
    stop_words = list(ENGLISH_STOP_WORDS)  # Convert set to list
    
    # Create a pipeline for feature extraction and topic modeling
    vectorizer = CountVectorizer(stop_words=stop_words)
    transformer = TfidfTransformer()
    lda = LatentDirichletAllocation(n_components=num_keywords, random_state=42)

    model = make_pipeline(vectorizer, transformer, lda)
    
    # Fit the model and transform the text to get keywords
    features = model.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    top_keywords_idx = features[0].argsort()[-num_keywords:][::-1]
    
    keywords = [feature_names[idx] for idx in top_keywords_idx]

    return keywords
