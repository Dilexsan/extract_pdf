import os
import re
import glob
import csv
from pdfminer.high_level import extract_text


def read_pdf_file(file):
    with open(file, "rb") as file_handle:
        text = extract_text(file_handle)
    # text = re.sub(r"[^a-zA-Z0-9\/\s.]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text


def get_all_judge_names(text):

    # words = word_tokenize(text)
    # filtered_words = [word for word in words if word in stop_words]
    # text = " ".join(filtered_words)
    pattern1 = r"(?:Before|BEFORE)\s*[:]\s*.*?(?:Counsel[s]?|COUNSEL[S]?)\s*[:]\s*"
    pattern2 = r"([A-Z]\s*[.]?\s*.*?\s*[,]?\s*J.?)"
    # pattern3 = r"([A-Z].*?J|J.)"
    # Use regular expression to find the text between "before" and "counsel"
    matches1 = re.findall(pattern1, text)
    # matches = " ".join(matches)
    # matches = re.findall(pattern2, matches)
    if not matches1:
        return ["0"]
    judge_name = []
    for i in matches1:
        cleaned_match = re.sub(r"Before|:|BEFORE|&", "", i)
        cleaned_match = " ".join(word.capitalize() for word in cleaned_match.split())
        name = re.findall(pattern2, cleaned_match)
        if name:
            judge_name.append(name)
        else:
            return ["1"]
    return judge_name


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
            judge_names.extend(get_all_judge_names(text))
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    # Write judge names to CSV
    with open("judgepractice.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Judge Name"])
        for judge_name in judge_names:
            csvwriter.writerow([judge_name])

    print(f"Extracted judge names have been written to judge1.csv")


if __name__ == "__main__":
    dir_path = "D:\d\Intern_works\Automation\\backend_automation\paralegal-backend-automation\ca_cases_new_website\ca_cases_2024\\august"
    main(dir_path)
