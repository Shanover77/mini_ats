""" 
    PURPOSE: The main purpose of this project is to give an ATS percent score, 
    that will compare all the resumes from the 'resumes' to all the job description text files in the 'jds' folder

"""
import docx 
import os
import glob
import transformer_keyextract
from tabulate import tabulate


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
    Get all MS Word files from a specified directory, excluding hidden files and files starting with ~.

    Parameters:
    - directory_path (str): The path of the directory to search for Word files.

    Returns:
    - List[str]: A list of file paths for MS Word files in the specified directory.
    """
    valid_file_extensions = ('.docx', '.doc')
    
    word_files = [
        file_path
        for file_path in glob.glob(os.path.join(directory_path, '*'))
        if not file_path.startswith('.') and not os.path.basename(file_path).startswith('~') and file_path.lower().endswith(valid_file_extensions)
    ]
    
    return word_files

def get_text_files(directory_path):
    # Get all text files
    word_files = glob.glob(os.path.join(directory_path, '*.txt'))

    # Check if any file has '_' in the front
    files_with_underscore = [file for file in word_files if os.path.basename(file).startswith('_')]

    # Return only the file with '_' in the front, if found
    if files_with_underscore:
        return files_with_underscore
    else:
        return word_files

def calculate_similarity_percentage(resume_keys, jd_keys):
    """
    Calculate and return the percentage of similarity between two lists of strings.

    Parameters:
    - resume_keys (List[str]): The first list of strings.
    - jd_keys (List[str]): The second list of strings.

    Returns:
    - float: The percentage of similarity between the two lists.
    """
    set1 = set(word.lower() for word in resume_keys)
    set2 = set(word.lower() for word in jd_keys)

    common_words = set1.intersection(set2)
    similarity_percentage = (len(common_words) / max(len(set2))) * 100

    return similarity_percentage

def calculate_similarity_and_missing_skills(resume_keywords, job_desc_keywords):
    """
    Calculate and return the percentage of similarity between two lists of keywords
    and the keywords missing from the first list.

    Parameters:
    - resume_keywords (List[str]): The list of keywords from the resume.
    - job_desc_keywords (List[str]): The list of keywords from the job description.

    Returns:
    - float: The percentage of similarity between the two lists.
    - List[str]: The keywords missing from the resume.
    """
    resume_set = set(word.lower() for word in resume_keywords)
    job_desc_set = set(word.lower() for word in job_desc_keywords)

    common_keywords = resume_set.intersection(job_desc_set)
    missing_keywords = job_desc_set.difference(resume_set)
    similarity_percentage = (len(common_keywords) / len(job_desc_set)) * 100 if job_desc_set else 0

    return similarity_percentage, list(missing_keywords), list(common_keywords)


def showIt(path, jd, sim, missing, common):
        if sim > 50:
            color = '\033[1;32m'  # Green for sim > 50
        elif 40 <= sim <= 50:
            color = '\033[1;33m'  # Yellow for 40 <= sim <= 50
        else:
            color = '\033[1;31m'  # Red for sim < 40

        sim = round(sim)
        small_text_start = '\033[2;37m'  # ANSI escape code for smaller text size
        small_text_end = '\033[0m'  # ANSI escape code to reset text formatting

        print(f'\n[RESULT: {path.ljust(40)} | {jd.ljust(20)} = {color}{str(sim)}%\033[0m \n Missing skills: {small_text_start}{missing} \n Common: {common} {small_text_end}')

def print_small_text(strings, file_path):
    """
    Print a list of strings in a smaller text size.

    Parameters:
    - strings (List[str]): The list of strings to be printed.
    - file_path (str): The path of the file associated with the strings.
    """
    small_text_start = '\033[2;37m'  # ANSI escape code for smaller text size
    small_text_end = '\033[0m'  # ANSI escape code to reset text formatting
    print('[keys of]' + file_path, end=' ')
    
    for string in strings:
        print(f"{small_text_start}{string}{small_text_end}", end=' ')


def display_list_of_lists(data, headers=None, table_format="grid"):
    """
    Display a list of lists in a tabular format.

    Args:
    - data (list of lists): The data to display in tabular format.
    - headers (list or None): Optional list of headers for the table.
    - table_format (str): The format of the table (default is "grid").
    """
    if headers is not None:
        print(tabulate(data, headers=headers, tablefmt=table_format))
    else:
        print(tabulate(data, tablefmt=table_format))


def init():
    print('works')

if __name__ == "__main__":
    all_files = get_word_files('resumes')

    brief = []
    for path in all_files:
        text = read_word_document(path)
        resume_keys = transformer_keyextract.extract_skills(text)
        print_small_text(resume_keys, path)

        jdFiles = get_text_files('jds')
        for jd in jdFiles:
            jdText = read_text_from_file(jd)
            jd_keys = transformer_keyextract.extract_skills(jdText)
            print_small_text(jd_keys, jd)

            sim, missing, common = calculate_similarity_and_missing_skills(resume_keys, jd_keys)
            brief.append([path, jd, sim, len(missing), len(common)])
            showIt(path, jd, sim, missing, common)            
    
    headers = ["Resume file", "JD File", "Similarity", "Missing", "Common"]
    display_list_of_lists(brief, headers=headers)

