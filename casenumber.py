import os
import re
import glob
import csv
import fitz  # PyMuPDF
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, words


def read_first_page_text(file):
    # Open the PDF file
    doc = fitz.open(file)

    # Extract text from the first page
    first_page_text = doc[0].get_text()
    doc.close()

    # Clean up text

    return first_page_text


def get_case_numbers(text):
    
    pattern1 = r"\b([A-Z]?.*?\d{2,4}/\d{2,4})\b"
    pattern2 = r"\b([A-Z].*?\d{2,4}-\d{2,4})\b"
    pattern3 = r"\b([A-Z]+/.*?/.*?/.*?/\d{2,4})\b"

    # Check pattern1 first
    matches = re.findall(pattern1, text)

    # If no matches found with pattern1, check pattern2
    if not matches:
        matches = re.findall(pattern2, text)

    # If still no matches found with pattern2, check pattern3
    if not matches:
        matches = re.findall(pattern3, text)

    return matches

def find_all_pdfs(dir_path):
    # Find all PDF files in the directory
    return glob.glob(os.path.join(dir_path, "*.pdf"))


def main(dir_path):
    list_of_pdfs = find_all_pdfs(dir_path)

    # Extract case numbers
    all_case_numbers = []
    for file in list_of_pdfs:
        try:
            text = read_first_page_text(file)
            case_numbers = get_case_numbers(text)
            if len(case_numbers) == 0:
                case_numbers.append("0")  # Append "0" if no case numbers are found
            elif len(case_numbers) > 1:
                case_numbers[0]  # Append "/" if more than one case number is found
            all_case_numbers.append(
                case_numbers[0]
            )  # Take only the first case number or the special value
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    # Write case numbers to CSV
    with open("casenumber.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Case Number"])
        for case_number in all_case_numbers:
            csvwriter.writerow([case_number])

    print(f"Extracted case numbers have been written to case_numbers.csv")


if __name__ == "__main__":
    dir_path = "D:\d\Intern_works\Automation\extract_pdf\ca_cases_new_website\ca_cases_2024\\april"
    main(dir_path)
