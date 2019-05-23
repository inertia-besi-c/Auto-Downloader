# --------------------------------------------------------------------------------------------------------------------------------------------------- #
"""
This following code was created and written by Emmanuel Ogunjirin.

The following code is used to pull data from a path specified in an android device, to a path specified on your system. This will pull all data from the host device, and sort them
based on your specification on your system. This code as of right now, also ignores any unauthorized messages as long as a previous connection had been made in the same network
from the system to the host device. The code will need some modification to work appropriately on your device. Please read the comments carefully and alter them as needed to your
specifications. The code comes as is and I am not liable for any damages incurred form usage. The Adb to Python script used is thanks to Swind Ou who allowed free usage and alteration
of the code.


INSTRUCTION: If the error "TERM Variable is not set" happens, you will need to go find "Edit Configuration" in settings, and allow "Emulate Terminal Output" then rerun the file.
***
Usually you can find the "Edit Configuration" setting by clicking on the file name towards the right corner of the screen, and then click on the "Edit Configuration" option, and enable
the terminal output emulation
***
"""
# ------------------------------------------------------------------INITIALIZATIONS------------------------------------------------------------------- #

from adb.client import Client as AdbClient      # Adb client that allows adb in python
import sys      # Allows access to system.
import os       # Operating system access
import datetime     # Gets the date and the time
import time     # Imports the system time

os.system('adb start-server')       # Automatically starts the adb server if it is not already running.

client = AdbClient(host="127.0.0.1", port=5037)     # Opens the adb gateway. Default is "127.0.0.1" and 5037
devices = client.devices()  # This calls adb devices to see all the devices connected

# ----------------------------------------------------------------------SET-UP----------------------------------------------------------------------- #

Deployment_Identification = "P3D1-Development"      # Name of the deployment

Watch_Main_Directory = "BESI-C"     # Name of the folder directory where all the data is stored on the watch
Base_Station_Directory = Deployment_Identification+"-Data"      # Name of the folder the data will be stored on the device.

Watch_Main_Directory_Path = "/sdcard/"+Watch_Main_Directory     # Absolute path to watch folder directory
Base_Station_Directory_Path = "/Users/emmanuelogunjirin/Desktop/"+Base_Station_Directory        # Absolute path to where you want to save the data
patient_subdirectory = Base_Station_Directory_Path + "/" + "Patient"        # This is the patient subdirectory
caregiver_subdirectory = Base_Station_Directory_Path + "/" + "Caregiver"        # This is the caregiver subdirectory

watch_count = 2     # Number of watch given to each individual
origin = None       # Initializes the origin variable
destination = None      # Initializes the destination variable
downloadtime = None     # Initializes the download time variable
previousrun = None      # Initializes the previous run variable
patient_1_time = "Never"       # Initializes the patient-1 variable
patient_2_time = "Never"       # Initializes the patient-2 variable
caregiver_1_time = "Never"     # Initializes the caregiver-1 variable
caregiver_2_time = "Never"     # Initializes the caregiver-2 variable

"""
Information about the watches go here. It appears in the format below. Make sure all information is exactly the same as those in Android Studios. 
        'Device-Identification': ['IP-Address of device', 'Device-Identification from Android Studios']
"""
Information = \
    {
        "Patient-1": ["192.168.60.100:5555", "Patient-Device"],        # The first patient watch information
        "Patient-2": ["192.168.60.102:5555", "Patient-Device-Unused"],      # The second patient watch information
        "Caregiver-1": ["192.168.60.101:5555", "Caregiver-Device"],     # The first caregiver watch information
        "Caregiver-2": ["192.168.60.103:5555", "Caregiver-Device-Unused"],      # The second caregiver watch information
    }

"""
Information about the file format on the device. It appears in the format below. Make sure all information is exactly the same as those in Android Studios. 
        'Type of file': ['Where the file is in the device', 'What the file is called in the device']
"""
File_Information = \
    {
        # "Accelerometer": ["Accelerometer", "Accelerometer_Data.csv"],     # This is the accelerometer data file
        "Battery": ["Device_Activity", "Battery_Activity.csv"],     # This is the battery data file
        "Pedometer": ["Device_Activity", "Pedometer_Data.csv"],     # This is the pedometer data file
        "Estimote": ["Estimote", "Estimote_Data.csv"],      # This is the estimote data file
        "Heart_Rate": ["Heart_Rate", "Heart_Rate_Data.csv"],        # This is the heart rate data file
        "Sensors": ["Device_Activity", "Sensor_Activity.csv"],      # This is the sensors data file
        "System": ["Device_Activity", "System_Activity.csv"],       # This is the system data file
        "EODUpdater": ["Device_Updater", "EODEMA_DailyActivity"],       # This is the end of day ema updater data file
        "StepUpdater": ["Device_Updater", "Step_Activity"],     # This is the step activity data file
        "Pain_EMA_Results": ["EMA_Results", "Pain_EMA_Results.csv"],        # This is the pain results data file
        "Followup_EMA_Results": ["EMA_Results", "Followup_EMA_Results.csv"],        # This is the followup results data file
        "EndOfDay_EMA_Results": ["EMA_Results", "EndOfDay_EMA_Results.csv"],        # This is the end of day results data file
        "Pain_EMA_Activity": ["EMA_Activities", "Pain_EMA_Activity.csv"],        # This is the pain activity data file
        "Followup_EMA_Activity": ["EMA_Activities", "Followup_EMA_Activity.csv"],        # This is the followup activity data file
        "EndOfDay_EMA_Activity": ["EMA_Activities", "EndOfDay_EMA_Activity.csv"],        # This is the end of day activity data file
    }

# ------------------------------------------------------------------------OPERATION--------------------------------------------------------------------- #


def clear():
    """
    This clears the output on the python console.
    :return: Returns none.
    """
    os.system('cls' if os.name == 'nt' else 'clear')        # Clears the output on the python console.


def connecttodevices():
    """
    This checks and connects to the devices in the deployment. It keeps a constant adb bridge to the device and reconnects if the bridge is cut.
    :return: Returns the number of devices currently connected and accessible to the system.
    """
    devices_count = 0       # Number of devices currently connected
    adbdevices = str(os.popen('adb devices').read())        # Calls the terminal to initiate the adb devices command and saves the output to a variable
    adbdevices_split = adbdevices.split()       # Splits the results of the output by spaces.

    for item in adbdevices_split:   # For every item in the split result
        if item == "device":        # Checks if the item has the string "device"
            devices_count += 1      # If it does, it adds one to the list of devices
        if "unauthorized" in adbdevices_split:      # If "unauthorized" is in the list
            os.system('adb kill-server')      # Terminal is called to kill the server and restart it.

    for key, value in Information.items():      # For every item in the watch list
        if str(value[0]) not in str(adbdevices):        # If the IP address listed is not in the string of adb devices
            print("Checking Connection to", key, "with IP-Address", value[0])       # Prints to the console.
            os.system('adb connect ' + str(value[0]))       # They system tries to connect to the missing device.

    clear()     # Calls the clear function
    return devices_count        # Returns the number of devices currently connected to the system.


def datetimelog(endfile, mode):
    """
    This gets the date and time and appends it to the files listed.
    :param endfile: The destination path where the file you want to work with is at.
    :param mode: The mode in which you want the data to be appended in "a"-append, "w"-write, "r"-read, and all other modes are supported
    :return: Does not return anything.
    """
    with open(endfile, str(mode)) as file:      # Opens the specified file
        current_time_download = datetime.datetime.now().strftime("%A %B %d %Y at %I:%M%p")        # Gets the current data and time from the system
        file.write("Last download run happened on " + str(current_time_download))        # Writes the line to the given device destination
        file.write("\n")        # Prints a new line


def dummyfile():
    """
    This creates the file in which the files where the data is stored.
    :return: Returns nothing.
    """
    global watch_count      # Global variable
    global Base_Station_Directory_Path      # Global variable
    global File_Information      # Global variable
    global patient_subdirectory     # Global variable
    global caregiver_subdirectory       # Global variable

    for information in Information:     # For every information given in the Information dictionary
        print("Creating files for", information)        # Prints to the console

        if not os.path.exists(patient_subdirectory) or not os.path.exists(caregiver_subdirectory):      # If the paths do not exist
            os.makedirs(patient_subdirectory)       # Makes the patient directory
            os.makedirs(caregiver_subdirectory)     # Makes the caregiver directory

        try:        # Tries to fo this
            while watch_count != 0:     # If the amount of devices connected is not 0
                for key, values in File_Information.items():        # For every file in the list

                    subdirectories = \
                        [
                            os.path.join(patient_subdirectory, Information["Patient-" + str(watch_count)][1] + "_" + values[1]),        # Path to patient directory
                            os.path.join(caregiver_subdirectory, Information["Caregiver-" + str(watch_count)][1] + "_" + values[1])     # Path to caregiver directory
                        ]

                    for path in subdirectories:     # For every file in the subdirectories
                        datetimelog(path, "w")      # Writes a log to the file

                watch_count -= 1        # Decreases the watch count
        except:     # If an error occurs
            print("Already have", information, "directory with files")      # Print this to the system


def pulldata():
    """
    Pulls the data from the devices listed, and puts them into the specified files made
    :return: Returns nothing
    """
    global device      # Global variable
    global origin      # Global variable
    global destination      # Global variable
    global patient_1_time
    global patient_2_time
    global caregiver_1_time
    global caregiver_2_time

    for device in devices:      # For every device listed in the devices dictionary
        print()     # Prints to the console
        print("Pulling data from", device.serial, "...")        # Prints to the console
        try:        # Tries the following
            for key, values in File_Information.items():        # For items in the file information dictionary
                current_time_pull = datetime.datetime.now().strftime("%A, %B %d %Y at %I:%M%p")  # Sets the current time variable

                if str(device.serial) == Information["Patient-1"][0]:       # If the device serial is the same as the ip address of the device for this watch
                    origin = str("/sdcard/BESI-C/" + values[0] + "/" + Information["Patient-1"][1] + "_" + values[1])       # This is where the file is on the host device
                    destination = str(Base_Station_Directory_Path + "/" + "Patient" + "/" + Information["Patient-1"][1] + "_" + values[1])      # This is where the file will be stored
                    device.pull(origin, destination)  # The files are pulled from the specific device with stated origin and destination
                    patient_1_time = current_time_pull      # Sets the patient-1 pull time
                elif str(device.serial) == Information["Patient-2"][0]:       # If the device serial is the same as the ip address of the device for this watch
                    origin = str("/sdcard/BESI-C/" + values[0] + "/" + Information["Patient-2"][1] + "_" + values[1])       # This is where the file is on the host device
                    destination = str(Base_Station_Directory_Path + "/" + "Patient" + "/" + Information["Patient-2"][1] + "_" + values[1])      # This is where the file will be stored
                    device.pull(origin, destination)  # The files are pulled from the specific device with stated origin and destination
                    patient_2_time = current_time_pull      # Sets the patient-2 pull time
                elif str(device.serial) == Information["Caregiver-1"][0]:       # If the device serial is the same as the ip address of the device for this watch
                    origin = str("/sdcard/BESI-C/" + values[0] + "/" + Information["Caregiver-1"][1] + "_" + values[1])       # This is where the file is on the host device
                    destination = str(Base_Station_Directory_Path + "/" + "Caregiver" + "/" + Information["Caregiver-1"][1] + "_" + values[1])      # This is where the file will be stored
                    device.pull(origin, destination)  # The files are pulled from the specific device with stated origin and destination
                    caregiver_1_time = current_time_pull      # Sets the caregiver-1 pull time
                elif str(device.serial) == Information["Caregiver-2"][0]:       # If the device serial is the same as the ip address of the device for this watch
                    origin = str("/sdcard/BESI-C/" + values[0] + "/" + Information["Caregiver-2"][1] + "_" + values[1])       # This is where the file is on the host device
                    destination = str(Base_Station_Directory_Path + "/" + "Caregiver" + "/" + Information["Caregiver-2"][1] + "_" + values[1])      # This is where the file will be stored
                    device.pull(origin, destination)  # The files are pulled from the specific device with stated origin and destination
                    caregiver_2_time = current_time_pull      # Sets the caregiver-2 pull time

                datetimelog(destination, "a")       # A log file with the data and time is appended to the end of the file.
                print("Data Pull Successful for", values[1])        # Prints to the console

        except:     # If any error happens in the process
            print("Device", device.serial, "is offline")        # Prints to the console


def runautodownloader():
    """
    This is the autodownloader that pulls the data and handles any error. The logic here uses the other functions created above.
    :return: Returns nothing.
    """
    global patient_subdirectory     # Global variable
    global caregiver_subdirectory       # Global variable

    current_timer = datetime.datetime.now().strftime("%A %B %d %Y at %I:%M%p")      # Sets the current time variable

    try:        # Tries to do the following
        connecttodevices()      # Calls the connect function
        print("Devices Check Done...")      # Prints to the console
    except:     # If any error happens in the process
        print("Devices Check Failed")       # Prints to the console

    if not os.path.exists(patient_subdirectory) or not os.path.exists(caregiver_subdirectory):      # If the paths do not exist
        try:        # Tries to do the following
            print("Running Files Setup")        # Prints to the console
            dummyfile()     # Calls the file creation function
            clear()     # Clears the console
            print("Initial Files Setup Successful")     # Prints to the console
        except:     # If any error happens in the process
            sys.exit("Failed Files Setup")      # The system exits the process with a error message on the console

    try:        # Tries to do the following
        pulldata()      # Calls the pull data function
        print()     # Prints to the console
        print("Data Pull Ended")        # Prints to the console
    except:     # If any error happens in the process
        sys.exit("Pull Data Failed")        # The system exits the process with a error message on the console

    print()     # Prints the console
    print("Last Download on", current_timer)     # Prints to the console


while True:     # Creates an always running loop
    current_time = datetime.datetime.now().strftime("%A, %B %d %Y at %I:%M%p")      # Sets the current time variable
    currentrun = connecttodevices()     # Sets the return of the connect function to the variable
    runs = [previousrun, currentrun]        # Keeps a running list of the number of devices from the last run, and the current run.

    if runs[0] != runs[1]:      # If the previous run and the current run do not have the same connected device count
        runautodownloader()     # Runs the autodownloader function
        previousrun, downloadtime = currentrun, current_time        # Sets the previous run value to the currentrun value, Sets a last download time for the system

    print()         # Prints to console
    print("Last Devices Check Occurred on", current_time)       # Prints to console
    print("Last Sync Attempted", downloadtime)       # Prints to console
    print()     # Prints to console
    print("Patient-1 Successfully Updated", patient_1_time)       # Prints to console
    print("Patient-2 Successfully Updated", patient_2_time)       # Prints to console
    print("Caregiver-1 Successfully Updated", caregiver_1_time)       # Prints to console
    print("Caregiver-2 Successfully Updated", caregiver_2_time)       # Prints to console
    print()       # Prints to console

    time.sleep(1)       # The system sleeps for the specified time
