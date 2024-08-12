import os
import re
import glob
import csv
from pdfminer.high_level import extract_text
from casenumber import find_all_pdfs,read_first_page_text,get_case_numbers 
from judge_practice import read_pdf_file,get_all_judge_names
from decided_on import get_decided_on

def case_number_dataframe(dir_path):
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

    return 


def judge_name_dataframe(dir_path):
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
    
    return 


def judgment_date_dataframe(dir_path):
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
    with open("decided.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Judgment date"])
        for judge_date in judgement_dates:
            csvwriter.writerow([judge_date])

    return 

def print_dataframe():
    
    return 



def main(dir_path):

    case_number_dataframe(dir_path)
    judge_name_dataframe(dir_path)
    judgment_date_dataframe(dir_path)
    print_dataframe()

    return
    
if __name__ == "__main__":
    dir_path = "D:\d\Intern_works\Automation\extract_pdf\ca_cases_new_website\ca_cases_2024\\april"
    main(dir_path)
