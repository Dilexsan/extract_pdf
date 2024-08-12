import os
import re
import glob
import csv
from pdfminer.high_level import extract_text


def read_pdf_file(file):
    with open(file, "rb") as file_handle:
        text = extract_text(file_handle)
    text = re.sub(r"\s+", " ", text)

    return text


def get_decided_on(text):

    pattern1 = r"(?:Decided on|DECIDED ON)\s*[:]\s*\d{2}.\d{2}.\d{4}"
    matches1 = re.findall(pattern1, text)

    if matches1:
        return matches1
    else:
        return ["0"]


def find_all_pdfs(dir_path):
    all_pdfs = glob.glob(os.path.join(dir_path, "*.pdf"))
    return all_pdfs


def main(dir_path):
    list_of_pdfs = find_all_pdfs(dir_path)

    # Extract judge names
    judge_names = []
    for file in list_of_pdfs:
        try:
            text = read_pdf_file(file)
            judge_names.extend(get_decided_on(text))
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    # Write judge names to CSV
    with open("decided.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Judge Name"])
        for judge_name in judge_names:
            csvwriter.writerow([judge_name])

    print(f"Extracted judge names have been written to judge1.csv")


if __name__ == "__main__":
    dir_path = "D:\d\Intern_works\Automation\extract_pdf\ca_cases_new_website\ca_cases_2024\\july"
    main(dir_path)
