import sqlite3

# Function to create the database and tables
def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('DDIS Prep FIle Archive.sqlite')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create Patient table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patient (
            UID INTEGER PRIMARY KEY,
            PatientID TEXT NOT NULL,
            PatientName TEXT NOT NULL
        )
    ''')

    # Create Study table with foreign key reference
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Study (
            id INTEGER PRIMARY KEY,
            PatientUID INTEGER,
            StudyID TEXT NOT NULL,
            StudyInstanceUID TEXT NOT NULL,
            Modality TEXT NOT NULL,
            ImportedPath TEXT NOT NULL,
            ImportedDate DATE,
            DirCount INTEGER NOT NULL,
            FilesCount INTEGER NOT NULL,
            ArchivePath TEXT NOT NULL,
            ArchiveDate DATE,
            FOREIGN KEY (PatientUID) REFERENCES Patient(UID)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data_into_database(patient_id, patient_name, study_id, study_instance_uid, modality, imported_path, imported_date, folder_count, files_count, archive_path, archive_date):
    conn = sqlite3.connect('DDIS Prep FIle Archive.sqlite')
    cursor = conn.cursor()

    # Check if the patient already exists in the Patient table
    cursor.execute("SELECT UID FROM Patient WHERE PatientID = ?", (patient_id,))
    patient_uid_result = cursor.fetchone()

    # If the patient does not exist, insert into the Patient table
    if not patient_uid_result:
        cursor.execute("INSERT INTO Patient (PatientID, PatientName) VALUES (?, ?)", (patient_id, patient_name))
        patient_uid = cursor.lastrowid
    else:
        patient_uid = patient_uid_result[0]

    # Insert data into the Study table with the foreign key reference
    cursor.execute("INSERT INTO Study (PatientUID, StudyID, StudyInstanceUID, Modality, ImportedPath, ImportedDate, DirCount, FilesCount, ArchivePath, ArchiveDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (patient_uid, study_id, study_instance_uid, modality, imported_path, imported_date, folder_count, files_count, archive_path, archive_date))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Create the database and tables
create_database()

