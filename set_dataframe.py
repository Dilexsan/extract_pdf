import os
import re
import glob
import csv
import pandas as pd
from pdfminer.high_level import extract_text
from casenumber import find_all_pdfs, read_first_page_text, get_case_numbers
from judge_practice import read_pdf_file, get_all_judge_names
from decided_on import get_decided_on

def case_number_dataframe(dir_path):
    list_of_pdfs = find_all_pdfs(dir_path)

    # Extract case numbers
    case_numbers = []
    for file in list_of_pdfs:
        try:
            text = read_first_page_text(file)
            case_nums = get_case_numbers(text)
            if len(case_nums) == 0:
                case_numbers.append("0")
            elif len(case_nums) > 1:
                case_numbers.append(case_nums[0])  # Take the first case number
            else:
                case_numbers.append(case_nums[0])
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    return case_numbers

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

    return judge_names

def judgment_date_dataframe(dir_path):
    list_of_pdfs = find_all_pdfs(dir_path)

    # Extract judgment dates
    judgment_dates = []
    for file in list_of_pdfs:
        try:
            text = read_pdf_file(file)
            judgment_dates.extend(get_decided_on(text))
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    return judgment_dates

def create_dataframe(dir_path):
    case_numbers = case_number_dataframe(dir_path)
    judge_names = judge_name_dataframe(dir_path)
    judgment_dates = judgment_date_dataframe(dir_path)

    # Create a Pandas DataFrame
    df = pd.DataFrame({
        'Case Number': case_numbers,
        'Judge Name': judge_names,
        'Judgment Date': judgment_dates
    })

    return df

def main(dir_path):
    df = create_dataframe(dir_path)
    df.to_csv("combined_data.csv", index=False)

    return

if __name__ == "__main__":
    dir_path = "D:\d\Intern_works\Automation\extract_pdf\ca_cases_new_website\ca_cases_2024\\april"
    main(dir_path)
