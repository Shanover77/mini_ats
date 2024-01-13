# Mini ATS in Python

## Purpose

The primary goal of this Python program is to provide an Applicant Tracking System (ATS) percent score by comparing the content of resumes (in the 'resumes' folder) to job description text files (in the 'jds' folder). The program utilizes keyword extraction to calculate the similarity percentage between the keywords in resumes and job descriptions.

## Features

- Reads both Microsoft Word (.docx, .doc) and plain text (.txt) files.
- Utilizes keyword extraction to identify important terms in the documents.
- Calculates the similarity percentage between resume and job description keywords.
- Displays the results with color-coded output for better visibility.

## How to Use

1. Create a folder named **resumes**.
   - This folder will contain all the MS Word documents representing resumes.

2. Create a folder named **jds**.
   - This folder will contain all the job description text files in .txt format.

3. Place all your MS Word documents (in .docx or .doc format) representing resumes in the **resumes** folder.

4. Place all your job description text files (in .txt format) in the **jds** folder.

5. Install dependencies using the following command:

    ```bash
    pip install -r requirements.txt
    ```

6. Run the program using `main.py`:

    ```bash
    python main.py
    ```

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`

## File Structure

- **resumes**: Contains all the resumes in either Word or plain text format.
- **jds**: Contains all the job description text files.

## Functions

### `read_text_from_file(file_path)`

Reads and returns the text content from a text file.

### `read_word_document(file_path)`

Reads and returns the text content from a Microsoft Word document.

### `get_word_files(directory_path)`

Gets all MS Word files from a specified directory.

### `get_text_files(directory_path)`

Gets all text files from a specified directory.

### `calculate_similarity_percentage(list1, list2)`

Calculates and returns the percentage of similarity between two lists of strings.

### `showIt(path, jd, sim)`

Displays the results with color-coded output based on the similarity percentage.

### `init()`

A placeholder function to initialize the program.

## Output Legend

- Green: Similarity > 50%
- Yellow: 40% <= Similarity <= 50%
- Red: Similarity < 40%

## Note

- Ensure that the 'resumes' and 'jds' folders contain the relevant files before running the script.

Feel free to customize the program according to your specific needs.
