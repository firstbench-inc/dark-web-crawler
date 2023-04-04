import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import string
import time

# Define the keyword to search for
keyword = "cocaine"

# Define the path to the directory containing the text files
folder_path = "/home/shusrith/filter-results"

# Create a list to store the file paths and text contents


# Iterate over the files in the directory


def search(sentences):
    path = "/home/shusrith/results.txt"
    # Create an instance of the TfidfVectorizer class and fit it to the preprocessed text data
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Get the index of the keyword in the feature matrix
    keyword_idx = vectorizer.vocabulary_.get(keyword)

    # Get the TF-IDF scores for the keyword across all sentences
    tfidf_scores = tfidf_matrix[:, keyword_idx].todense()

    # Find the sentences that contain the keyword or related words
    related_sentences = []
    for i, score in enumerate(tfidf_scores):
        if score > 0:
            related_sentences.append(sentences[i])

    # Print the related sentences
    with open("/home/shusrith/sentences.txt", "a") as f:
        f.write(f"in {path}\n")
        for i in related_sentences:
            f.write(f"{i}\n")


def lsa(file_contents, file_path, sentences):
    # Create a TF-IDF vectorizer and fit it to the text contents
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform(file_contents)
    except:
        # print(file_path)
        # time.sleep(10)
        return 0

    # Transpose the TF-IDF matrix to ensure it is square
    tfidf_matrix_transposed = tfidf_matrix.T

    # Create an LSA model and fit it to the transposed TF-IDF matrix
    lsa_model = TruncatedSVD(n_components=10)
    try:
        lsa_matrix = lsa_model.fit_transform(tfidf_matrix_transposed)
    except:
        # print("some error happened in ", file_path, ", continuing")
        return 0

    # Find the index of the keyword in the vocabulary
    keyword_index = vectorizer.vocabulary_.get(keyword, None)
    if keyword_index is None:
        # print(f"The keyword '{keyword}' is not present in the text files.")
        return 0
    else:
        # Get the row of the LSA matrix corresponding to the keyword
        keyword_row = lsa_matrix[keyword_index, :]

        # Compute the cosine similarity between the keyword row and all other rows
        similarity_scores = np.dot(lsa_matrix, keyword_row) / (
            np.linalg.norm(lsa_matrix, axis=1) * np.linalg.norm(keyword_row)
        )

        # Sort the files by decreasing similarity score
        sorted_indices = np.argsort(similarity_scores)[::-1]
        sorted_files = [file_contents[i] for i in sorted_indices]
        print(len(sorted_indices), len(file_contents))

        # Print the sorted files and similarity scores
        with open("/home/shusrith/results.txt", "a") as f:
            # f.write(f"in {file_path}\n")
            # for i in range(len(sorted_files)):
            # f.write(
            #     f"{sorted_files[i]}: {similarity_scores[sorted_indices[i]]:.2f}\n"
            # )
            f.write(f"{file_path}\n")
        # f.write("\n\n\n")

        search(sentences)
        return 1


a = 0
b = 0
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt"):
        # If the file is a text file, read its contents and store the path and content
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r") as f:
            text = f.read()
            file_text = text.split()
            
            sentences = text.split(".")
            sentences = [s.lower().strip().translate(str.maketrans("", "", string.punctuation))for s in sentences]
     
            a += lsa(file_text, file_path, sentences)
        # print(a)
    b += 1

print(f"Found {a} results in {b} entries")
