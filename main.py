
import os
import shutil
import pandas as pd
import sqlite3
from loguru import logger
from dotenv import load_dotenv
from datetime import datetime
from support import db_read, count_folders_and_files, copy_files_make_zip, process_path
from dbconnection import insert_data_into_database

load_dotenv()
dbpath = os.getenv("dbpath")
root_dir = os.getenv("root_dir")
output_dir = os.getenv("output_dir")


start_of_day = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
log_filename = os.path.join("logs", f"{start_of_day.strftime('%Y-%m-%d')}.log")
# os.makedirs(log_directory, exist_ok=True)  # Create the directory if it doesn't exist
# log_filename = os.path.join(log_directory, "logfile.log")

# Configure Loguru logger in append mode
logger.add(
    log_filename, mode="a", level="DEBUG", 
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    )


def dicom_with_zip(dbpath, root_dir, output_dir, date):
    try:
        # date = datetime(2023, 11, 8).date()
        data = db_read(dbpath) # read sql
        data['ProcessedPath'] = data['Filename'].map(lambda x: process_path(x))
        data['DisplayedFieldsUpdatedTimestamp_x'] = pd.to_datetime(data['DisplayedFieldsUpdatedTimestamp_x'])
        fdata = data[data['DisplayedFieldsUpdatedTimestamp_x'].dt.date == date]

        for index, row in fdata.iterrows():
            if "dicom" in  row['ProcessedPath']:
                folder_dir = os.path.join(root_dir, row['ProcessedPath'])
                dir, files = count_folders_and_files(folder_dir)

                patient_id = row['PatientID']
                patient_name = row['PatientsName']
                study_id = row['StudyID']
                study_instance_uid = row['StudyInstanceUID']
                modality = row['Modality']
                imported_path = folder_dir
                imported_date = row['DisplayedFieldsUpdatedTimestamp_x'].strftime('%Y-%m-%d %H:%M:%S')
                folder_count = dir
                files_count = files
                archive_path = os.path.join(output_dir, f"{patient_id} {patient_name} {modality} {study_id}")
                archive_date = datetime.today()

                copy_files_make_zip(
                    root_dir=folder_dir,
                    output_dir=output_dir,
                    patient_id=patient_id,
                    patient_name=patient_name,
                    modality=modality,
                    study_id=study_id,
                    date=archive_date
                )

                insert_data_into_database(
                    patient_id=patient_id,
                    patient_name=patient_name,
                    study_id=study_id,
                    study_instance_uid=study_instance_uid,
                    modality=modality,
                    imported_path=imported_path,
                    imported_date=imported_date,
                    folder_count=folder_count,
                    files_count=files_count,
                    archive_path=archive_date,
                    archive_date=archive_date
                )
                
                info = {
                    "filename": row['ProcessedPath'],
                    "Patient ID": row['PatientID'],
                    "patient name": row['PatientsName'],
                    "count": (dir, files),
                    "importeddate": row['DisplayedFieldsUpdatedTimestamp_x']
                }

                logger.info(info)

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
   
# date = datetime(2023, 11, 8).date()
date = datetime.today().date()
dicom_with_zip(dbpath, root_dir, output_dir, date)
