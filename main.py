""" 
    PURPOSE: The main purpose of this project is to give an ATS percent score, 
    that will compare all the resumes from the 'resumes' to all the job description text files in the 'jds' folder

"""
import docx 
import os
import glob
import keywords

def read_text_from_file(file_path):
    """
    Read and return the text content from a text file.

    Parameters:
    - file_path (str): The path of the text file to be read.

    Returns:
    - str: The text content read from the specified file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()
    return text_content

def read_word_document(file_path):
    try:
        doc = docx.Document(file_path)
        text = []

        for paragraph in doc.paragraphs:
            text.append(paragraph.text)

        return '\n'.join(text)
    except Exception as e:
        return f"An error occurred: {e}"


def get_word_files(directory_path):
    """
    Get all MS Word files from a specified directory.

    Parameters:
    - directory_path (str): The path of the directory to search for Word files.

    Returns:
    - List[str]: A list of file paths for MS Word files in the specified directory.
    """
    word_files = glob.glob(os.path.join(directory_path, '*.docx')) + glob.glob(os.path.join(directory_path, '*.doc'))
    return word_files

def get_text_files(directory_path):
    # get all text files

    word_files = glob.glob(os.path.join(directory_path, '*.txt'))
    return word_files

def calculate_similarity_percentage(list1, list2):
    """
    Calculate and return the percentage of similarity between two lists of strings.

    Parameters:
    - list1 (List[str]): The first list of strings.
    - list2 (List[str]): The second list of strings.

    Returns:
    - float: The percentage of similarity between the two lists.
    """
    set1 = set(word.lower() for word in list1)
    set2 = set(word.lower() for word in list2)

    common_words = set1.intersection(set2)
    similarity_percentage = (len(common_words) / max(len(set1), len(set2))) * 100

    return similarity_percentage

def showIt(path, jd, sim):
        if sim > 50:
            color = '\033[1;32m'  # Green for sim > 50
        elif 40 <= sim <= 50:
            color = '\033[1;33m'  # Yellow for 40 <= sim <= 50
        else:
            color = '\033[1;31m'  # Red for sim < 40

        print(f'Resume {path.ljust(40)} | {jd.ljust(20)} = {color}{str(sim)}%\033[0m')

def init():
    print('works')

if __name__ == "__main__":
    all_files = get_word_files('resumes')
    for path in all_files:
        text = read_word_document(path)
        resume_keys = keywords.extract_keywords(text, 100)

        jdFiles = get_text_files('jds')
        for jd in jdFiles:
            jdText = read_text_from_file(jd)
            jd_keys = keywords.extract_keywords(jdText, 100)

            sim = calculate_similarity_percentage(resume_keys, jd_keys)
            showIt(path, jd, sim)            


