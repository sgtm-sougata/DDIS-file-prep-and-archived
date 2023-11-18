# DDIS Archive File Preparation

The **DDIS-Archive-file-Preparation** project streamlines and automates the archiving process, simplifying the upload to DDIS.

Follow these steps to set up and use the project:

### Step 1: Install Python

Download and install Python's latest version from [python.org](https://www.python.org/downloads/).

### Step 2: Clone the Repository

Clone the project repository to your local drive:

```bash
git clone https://github.com/CHAVI-India/DDIS-Archive-file-Preparation.git

```

### Step 3: Set Up Environment
Install Python and ensure it is added to the system's environment path during installation.

### Step 4: Configure .env File
Navigate to the project directory (DDIS-Archive-file-Preparation) and edit the .env file

```bash
# .env file

# Database path
dbpath = "sqlite:///D:/DICOM DATABASE/DICOM IMPORT/ctkDICOM.sql"

# DICOM import directory path
root_dir = "D:\\DICOM DATABASE\\DICOM IMPORT"

# Output directory path for saving Archive
output_dir = "D:\\python\\ddis zip testing"
```
### Step 5: Update script.bat File
Edit the script.bat file with the correct paths

```bash
# REM script.bat

# Project Virtual env path
set VENV_PATH=D:\python\FIle prep DDIS\venv\Scripts\activate

# Add start (where main.py) path
cd /d D:\python\FIle prep DDIS

```

### Step 6: Schedule the Task
Open Task Scheduler.
- Go to Action and click "Create Task."
- Fill in task details and set triggers according to your requirements.
- In the Action tab, click "New," then browse and select script.bat. Save the changes.

### Step 7: Verify SQLite Data
Download an SQLite viewer or use Visual Studio Code with the SQLite extension to inspect the data.

Need Help?
If you encounter any issues or have questions, please contact Sougata Maity at maitysougata724@gmail.com.

