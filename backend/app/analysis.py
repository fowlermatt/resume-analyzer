import yake
import spacy
import re

try:
    nlp = spacy.load("en_core_web_sm")
    print("spaCy model 'en_core_web_sm' loaded successfully.")
except OSError:
    print("spaCy model 'en_core_web_sm' not found. Please run:")
    print("python -m spacy download en_core_web_sm")
    nlp = None 


kw_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=30, features=None)

def extract_keywords_yake(text: str) -> set[str]:
    if not text:
        return set()
    try:
        keywords_with_scores = kw_extractor.extract_keywords(text)
        return {kw.lower() for kw, score in keywords_with_scores}
    except Exception as e:
        print(f"Error during YAKE keyword extraction: {e}")
        return set()


def extract_entities_spacy(text: str) -> set[str]:
    if not text or not nlp:
        return set()
    text = re.sub(r'\s+', ' ', text).strip()
    doc = nlp(text)
    entities = set()
    relevant_labels = {"ORG", "PRODUCT", "NORP", "WORK_OF_ART", "PERSON"}
    for ent in doc.ents:
        if ent.label_ in relevant_labels:
            entities.add(ent.text.lower())
    return entities


def extract_combined_keywords(text: str) -> set[str]:
    yake_keywords = extract_keywords_yake(text)
    combined = yake_keywords
    return combined


def compare_keywords(resume_keywords: set[str], jd_keywords: set[str]) -> dict:
    if not isinstance(resume_keywords, set): resume_keywords = set(resume_keywords)
    if not isinstance(jd_keywords, set): jd_keywords = set(jd_keywords)

    matched_keywords = list(jd_keywords.intersection(resume_keywords))
    missing_keywords = list(jd_keywords.difference(resume_keywords))


    match_score = 0
    if jd_keywords:
        match_score = round((len(matched_keywords) / len(jd_keywords)) * 100)
    else:
        if not resume_keywords:
             match_score = 100

    return {
        "match_score": match_score,
        "matched_keywords": sorted(matched_keywords),
        "missing_keywords": sorted(missing_keywords),
    }