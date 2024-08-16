import os
import re
import glob
import csv
from pdfminer.high_level import extract_text
import pdfplumber

# def read_pdf_file(file):
#     with open(file, "rb") as file_handle:
#         text = extract_text(file_handle)
#     text = re.sub(r"\s+", " ", text)
    
#     return text

def read_pdf_file(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            cropped_page = page.crop((0, 80, page.width, page.height - 80))
            text += cropped_page.extract_text()
        text = re.sub(r"\s+", " ", text)
    return text

# def get_counsel(text):

#     #text = text.lower()
#     pattern1 = r"(?:counsel[s]?)\s*[:]\s*(.*?)\s*:"
#     pattern2 = r"(?:argued on|supported on|inquiry on)"

#     matches1 = re.findall(pattern1, text,re.IGNORECASE)
#     if matches1:
#         cleaned_matches = []
#         cleaned_match = re.sub(pattern2, "", matches1[0],flags=re.IGNORECASE)
#         cleaned_matches.append(cleaned_match)
#         return cleaned_matches
#     return ["0"]

def get_counsel(text):

    #text = text.lower()
    pattern = r"Written Submissions?.*?\s*:\s*(.*?)(?=\b(?:Argued on|Decided on|Supported on|Inquiry on)\s*:\s*\b)"

    matches1 = re.findall(pattern, text,re.IGNORECASE)
    if matches1:
        cleaned_matches = []
        cleaned_matches.append(matches1[0])
        return cleaned_matches
    return ["0"]


def find_all_pdfs(dir_path):
    all_pdfs = glob.glob(os.path.join(dir_path, "*.pdf"))
    return all_pdfs


def main(dir_path):
    list_of_pdfs = find_all_pdfs(dir_path)

    # Extract judge names
    counsels = []
    for file in list_of_pdfs:
        try:
            text = read_pdf_file(file)
            counsels.extend(get_counsel(text))
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    # Write judge names to CSV
    with open("written.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Counsel Members"])
        for counsel in counsels:
            csvwriter.writerow([counsel])

    print(f"Extracted counsel have been written to decided.csv")


if __name__ == "__main__":
    dir_path = "D:\d\Intern_works\Automation\extract_pdf\ca_cases_new_website\ca_cases_2024\\june"
    main(dir_path)
