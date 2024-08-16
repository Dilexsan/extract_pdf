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
            text += page.extract_text()
        text = re.sub(r"\s+", " ", text)
    return text


def get_decided_on(text):
    text = text.lower()

    pattern1 = r"(?:written submissions|written submissions on)\s*[:]\s*(\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4})"
    pattern2 = r"(?:written submissions|written submissions on)\s*[:]\s*(\d{1,2}.*?\d{4})"
    matches1 = re.findall(pattern1, text)
    matches2 = re.findall(pattern2, text)

    dates = []
    if matches1:
        dates.append(matches1[0])
        
    elif matches2:  
        dates.append(matches2[0])
    else:
        dates.append("0")
       
    return dates


def find_all_pdfs(dir_path):
    all_pdfs = glob.glob(os.path.join(dir_path, "*.pdf"))
    return all_pdfs


def main(dir_path):
    list_of_pdfs = find_all_pdfs(dir_path)

    # Extract judge names
    judgement_dates = []
    for file in list_of_pdfs:
        try:
            text = read_pdf_file(file)
            judgement_dates.extend(get_decided_on(text))
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    # Write judge names to CSV
    with open("written.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Judgment date"])
        for judgement_date in judgement_dates:
            csvwriter.writerow([judgement_date])

    print(f"Extracted judgment dates have been written to decided.csv")


if __name__ == "__main__":
    dir_path = "D:\d\Intern_works\Automation\extract_pdf\ca_cases_new_website\ca_cases_2024\\may"
    main(dir_path)
