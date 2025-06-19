# STag-detector-post-recording Installation and Use Instructions

## Installation
### Step 1: Download repository
1.	click the green ‘<> Code’ button on [STag-detector-post-recording](github.com/JulianKempenaers/Stag-detector-post-recording) and select ‘download ZIP’. 
2.	Locate the zipped folder in your downloads and unzip it to your desired location on your computer. 

### Step 2: Create an environment and install packages 
Windows:

3.	Open your Windows Command Prompt
  
4. 	Ensure you have python installed. This can be checked by typing  <pre> ```python -–version``` </pre>   if it says python was not found, install python from [python.org](https://www.python.org/). Note, when you open the installer, check the ‘Add to path’ box before clicking install. 

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


