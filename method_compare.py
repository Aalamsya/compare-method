import os
import nltk
# nltk.download('omw-1.4')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
import numpy as np
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess(text):
    sentences = nltk.sent_tokenize(text)
    words = [nltk.word_tokenize(sentence) for sentence in sentences]
    pos_tags = []
    for sentence in words:
        pos = nltk.pos_tag(sentence)
        # Only append tuples with a word and its corresponding part-of-speech tag
        pos_tags += [p for p in pos if len(p) == 2]
    return pos_tags




def semantic_similarity(synset1, synset2):
    if synset1 is None or synset2 is None:
        return 0

    return synset1.path_similarity(synset2)


def semantic_link_network(pos_tags1, pos_tags2):
    similarity_matrix = np.zeros((len(pos_tags1), len(pos_tags2)))

    for i, pos_tag1 in enumerate(pos_tags1):
        for j, pos_tag2 in enumerate(pos_tags2):
            word1, pos1 = pos_tag1
            word2, pos2 = pos_tag2
        
            if pos1.startswith('J'):
                pos1 = 'a'
                synset1 = wn.synsets(word1, pos=pos1) 
            else: 
                 synset1 = None
            
            if pos2.startswith('J'):
                pos2 = 'a'
                synset2 = wn.synsets(word2, pos=pos2) 
            else: 
                synset2 = None

        if synset1 and synset2:
            max_similarity = max(
                semantic_similarity(s1, s2) for s1 in synset1 for s2 in synset2
            )
            similarity_matrix[i, j] = max_similarity

    return similarity_matrix.mean()


def cosine_similarity_func(text1, text2):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


def compare_texts(documents, questions):
  

    n_docs = len(documents)
    n_qs = len(questions)

    sln_similarities = np.zeros((n_docs, n_qs))
    cosine_sims = np.zeros((n_docs, n_qs))

    for i, document in enumerate(documents):
        pos_tags1 = preprocess(document)
        for j, question in enumerate(questions):
            pos_tags2 = preprocess(question)

            sln_similarity = semantic_link_network(pos_tags1, pos_tags2)
            cosine_sim = cosine_similarity_func(document, question)

            sln_similarities[i, j] = sln_similarity
            cosine_sims[i, j] = cosine_sim

    return sln_similarities, cosine_sims


if __name__ == "__main__":
    # Replace these with the paths to your document and question files
    document_dir = r"D:\Kuliah\sl\experimental result QA\ull data\data_collection\data_collection\All_Article\1-100"
    question_dir = r"D:\Kuliah\sl\experimental result QA\ull data\data_collection\data_collection\questionOfXlsx\1-100"

    documents = []
    questions = []

    for filename in os.listdir(document_dir):
        with open(os.path.join(document_dir, filename), "r", encoding="latin-1") as f:
            document = f.read()
            documents.append(document)

    for filename in os.listdir(question_dir):
        with open(os.path.join(question_dir, filename), "r", encoding="latin-1") as f:
            question = f.read()
            questions.append(question)

    sln_similarity, cosine_sim = compare_texts(documents, questions)


print(f"Semantic Link Network Similarity: {sln_similarity[0, 0]:.2f}")
print(f"Cosine Similarity: {cosine_sim[0, 0]:.2f}")