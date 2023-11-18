
import os
import re
import shutil
import pydicom
import pandas as pd
from datetime import datetime

def db_read(dbpath):
    """
    Read data from the specified SQLite database file and perform necessary data processing.

    Parameters:
    - dbpath (str): Path to the SQLite database file.

    Returns:
    - pd.DataFrame: Processed DataFrame containing relevant information from the database.

    This function reads tables from an SQLite database file, performs joins and filtering,
    and returns a DataFrame with selected columns.

    """
    try:
        # Read Images, Series, Studies, and Patients tables from the database
        images = pd.read_sql_table("Images", dbpath)
        series = pd.read_sql_table("Series", dbpath)

        study_selected_columns = ['StudyInstanceUID', 'StudyID', 'PatientsUID']
        studies = pd.read_sql_table("Studies", dbpath, columns=study_selected_columns)

        patients_selected_columns = ['UID', 'PatientID', 'PatientsName']
        patients = pd.read_sql_table("Patients", dbpath, columns=patients_selected_columns)

        # Unique Series Instance UID in Images table
        unique_images = images.drop_duplicates("SeriesInstanceUID")

        # join unique_images dataframe and series table based on the SeriesInstanceUID
        images_series = pd.merge(unique_images, series, on="SeriesInstanceUID", how="inner")

        # join images_series dataframe and studies table based on the StudyInstanceUID
        images_series_studies = pd.merge(studies, images_series, on="StudyInstanceUID", how="inner")
        unique_images_series_studies = images_series_studies.drop_duplicates("StudyInstanceUID")

        unique_images_series_studies_patients = pd.merge(unique_images_series_studies, patients, left_on="PatientsUID", right_on="UID", how="inner")

        colnames = ["PatientsUID", "PatientsName", "PatientID", "SOPInstanceUID", "StudyInstanceUID", "SeriesInstanceUID", "StudyID", "Modality", "Filename", "DisplayedFieldsUpdatedTimestamp_x"]
        db_info_ = unique_images_series_studies_patients[colnames]
        db_info = db_info_.drop_duplicates("StudyID")

        # db_info['DisplayedFieldsUpdatedTimestamp_x'] = pd.to_datetime(db_info['DisplayedFieldsUpdatedTimestamp_x'])

        # Print or use the DataFrame as needed
        return db_info

    except Exception as e:
        # Handle any exceptions that might occur during data processing
        print(f"DB connection and processing: {e}")
        return None


def count_folders_and_files(directory):
    """
    Count the total number of folders and files within a given directory.
    
    Parameters:
    - directory (str): The path to the root directory.
    
    Returns:
    - tuple: A tuple containing the total number of folders and files.
    """
    total_folders = 0
    total_files = 0

    for root, dirs, files in os.walk(directory):
        total_folders += len(dirs)
        total_files += len(files)

    return total_folders, total_files

def clean_filename(name):
    """
    Cleans a filename by replacing disallowed characters with underscores.
    
    Args:
        name (str): The input filename.

    Returns:
        str: The cleaned filename with disallowed characters replaced by underscores.
    """
    # Specify the characters you want to replace in the pattern
    pattern = r'[<>:"\\/|?*]'
    replacement = '_'

    # Use re.sub to replace consecutive occurrences of the specified characters with a single '_'
    result = re.sub(r'[_]+', '_', re.sub(pattern, replacement, name))

    # Trim leading and trailing underscores
    result = result.strip('_')

    return result


def copy_files_make_zip(root_dir, output_dir, patient_id, patient_name, modality, study_id, date):
    """
    Copy DICOM files from multiple folders within a specified root directory to a patient-specific directory,
    and create a ZIP archive of the copied files.

    Parameters:
    - root_dir (str): The root directory containing DICOM files.
    - patient_id (str): The unique identifier for the patient.
    - patient_name (str): The name of the patient.
    - date (str): The date for creating a patient-specific subdirectory.
    """

    formatted_date = date.strftime("%d_%m_%Y")
    patient_dir = os.path.join(root_dir, patient_name, formatted_date)
    # patient_id_ = clean_filename(patient_id)
    patient_id_ = re.sub('/', '_', patient_id)
    zip_name_with_path = os.path.join(output_dir, formatted_date, f"{patient_id_} {patient_name} {modality} {study_id}")

    for path, dirs, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(path, filename)
            try:
                dcm = pydicom.dcmread(filepath)
                patient_id = dcm.PatientID
                sopinstanceuid = dcm.SOPInstanceUID

                os.makedirs(patient_dir, exist_ok=True)
                shutil.copy(filepath, os.path.join(patient_dir, f"{sopinstanceuid}_{filename}"))
                
            except Exception as e:
                print(f"Error: {e} - File: {filename}")

    shutil.make_archive(base_name=zip_name_with_path, format="zip", root_dir=patient_dir)
    shutil.rmtree(os.path.join(root_dir, patient_name))


def process_path(filename):
    """
    Process a filename to extract a specific path.

    Parameters:
    - filename (str): The input filename.

    Returns:
    - str: The processed path extracted from the filename. If no match is found, returns "No match found."

    This function takes a filename as input and attempts to match a specific pattern in it.
    If a match is found, it extracts a portion of the path and performs a substitution to replace '/' with '//'.
    The processed path is then returned. If no match is found, the function returns "No match found."

    Example:
    processed_path = process_filename("example/path/to/file.txt")
    print(processed_path)  # Output: "example//path"
    """
    match = re.match(r'([^/]+/[^/]+)', filename)

    if match:
        extracted_path = match.group(1)
        extracted_path = re.sub("/", "//", extracted_path)
        return extracted_path
    else:
        return "No match found."



