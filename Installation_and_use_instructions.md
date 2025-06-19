# STag-detector-post-recording Installation and Use Instructions

# Windows: (Scroll down for macOS)

## Installation
### Step 1: Download repository
1.	click the green ‘<> Code’ button on [STag-detector-post-recording](github.com/JulianKempenaers/Stag-detector-post-recording) and select ‘download ZIP’. 
2.	Locate the zipped folder in your downloads and unzip it to your desired location on your computer. 

### Step 2: Create an environment and install packages 
3.	Open your Windows Command Prompt
  
4. 	Ensure you have python installed. This can be checked by typing  <pre> ```python -–version``` </pre>   if python was not found, install python from [python.org](https://www.python.org/). Note, when you open the installer, check the ‘Add to path’ box before clicking install. 

5.	Navigate to where you saved the folder: <pre> ```cd path/to/your/STag-detector-post-recording-main``` </pre>
6.	Create a virtual environment named STag-detector-post-recording_env . <pre> ```python -m venv STag-detector-post-recording_env``` </pre>
7.	Activate the virtual environment <pre> ```.\STag-detector-post-recording_env\Scripts\Activate.bat``` </pre>
8.	Upgrade pip (optional but recommended) <pre> ```python -m pip install --upgrade pip ``` </pre>
9.	Install required packages <pre> ```pip install -r requirements.txt ``` </pre>


## Running the software

There are two options:
### Option 1: Via your command prompt window
1. Repeat steps 3, 5 and 7 from the installation step
2. Then, run this in that same command prompt   <pre> ```Main.py``` </pre>


### Option 2: By creating a .bat file.
To avoid having to type out these steps every single time, you can create a .bat file. This file will allow you to run the code simply by double clicking it. 

1. Open the STag-detector-post-recording-main folder and create a new .txt file inside it.
2. Open the txt file and copy-paste this into it:
 ```bash#
 @echo off
 cd /d C:\Users\jkemp\Desktop\VisionGroup\STag-detector-post-recording-main || (
   echo Failed to change directory.
   pause
   exit /b 1
 )
 call .\STag-detector-post-recording_env\Scripts\Activate.bat
 python Main.py
 echo.
 echo Press any key to close this window...
 pause
```
3. Change the line starting with `cd` to the same directory you used in step 5 of the installation process (note the backslashes `\`) and keep the `/d` between `cd` and the path. For example:  
`cd /d C:\path\to\your\STag-detector-post-recording-main`
4. Save file as `run_STag_detector.bat` (note, change ‘Save as type’ option from `Text document` to `All files (*.*)`)
5. Now you can run the detector simply by double-clicking the `run_STag_detector.bat` file. This file can be copied to your Desktop or any other convenient location as a shortcut to start running the code. 


# macOS
## Installation

### Step 1: Download repository
1. Click the green ‘<> Code’ button on [STag-detector-post-recording](https://github.com/JulianKempenaers/STag-detector-post-recording) and select ‘Download ZIP’.  
2. Locate the zipped folder in your Downloads and unzip it to your desired location (e.g., Documents or Desktop).

### Step 2: Create an environment and install packages  
macOS:

3. Open the **Terminal** application (found via Spotlight or in `Applications > Utilities`).

4. Check if Python is installed by typing:  ```python3 --version``` If python was not found, install python from [python.org](https://www.python.org/). Note, when you open the installer, check the ‘Add to path’ box before clicking install. 

5. Navigate to the folder you unzipped: <pre> ```cd /path/to/your/STag-detector-post-recording-main ``` </pre> tip: you can type cd and then drag the folder into Terminal to auto-fill the path
6. Create a virtual environment <pre> ```python3 -m venv STag-detector-post-recording_env```</pre>
7. Activate the virtual environment: <pre> ```source STag-detector-post-recording_env/bin/activate```</pre>
8. Upgrade pip (optional but recommended) <pre> ```python3 -m pip install --upgrade pip```</pre>
9. Install required packages <pre>```pip install -r requirements.txt```</pre>

## Running the software
There are two options:

### Option 1: Via the Terminal

1. Repeat steps 3, 5 and 7 from the Installation process
2. run the script: <pre> ``` python Main.py ```</pre>

### Option 2: By creating a shell script (.sh) file
To avoid repeating the above every time, you can automate it with a script:
1. Open the STag-detector-post-recording-main folder and create a new .txt file inside it.
2. Open the txt file and copy-paste this into it:
```bash
#!/bin/bash
cd /path/to/your/STag-detector-post-recording-main || {
  echo "Failed to change directory."
  exit 1
}
source STag-detector-post-recording_env/bin/activate
python Main.py
echo
echo "Press [Enter] to close..."
read
```
3. Replace `/path/to/your/...` with your actual folder path (same as Step 5 of installation instructions).
4. Save file as `run_STag_detector.sh` (note, change ‘Save as type’ option from `Text document` to `All files (*.*)`)
5. Now you can run the detector simply by double-clicking the `run_STag_detector.sh` file. This file can be copied to your Desktop or any other convenient location as a shortcut to start running the code. 








