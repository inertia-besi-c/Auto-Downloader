#!/usr/bin/env bash

echo "Indexing to Specified Directory..."       # Messages

cd  $HOME       # Heads to the home directory
cd "Box Sync"       # Indexes to the directory on the computer
cd "University of Virginia"     # Indexes to the directory on the computer
cd "Link Lab"       # Indexes to the directory on the computer
cd "Android Studios"        # Indexes to the directory on the computer
cd BESI     # Indexes to the directory on the computer
cd "BESI Cancer"        # Indexes to the directory on the computer

mkdir "BESI-C DATA"     # Makes a directory specified
cd "BESI-C DATA"        # Indexes to the directory on the computer

echo "Waiting for Command ..."      # Message
echo "Running ADB Devices..."       # Message

FILE="$(adb devices)"       # Sets FILE to the command for ADB devices.
echo "$(adb devices)"       # Message
FILES="${FILE//List of devices attached/}"      # Removes the header from the output

echo "Isolating Device(s) SERIAL_ID CODE..."        # Isolates the Serial ID of the device
SERIAL_ID="${FILES//device/}"       # Removes the device tag from the output
echo $SERIAL_ID     # Message

echo "Running Data Collection Code..."      # Message

for device in $SERIAL_ID; do        # For every device listed in adb devices
echo "Device: $device"      # Message
echo "Acquiring Data from $device..."       # Message
echo "Running Extraction File in $device..."        # Message
mkdir "$device"     # Makes a directory with the serial number of the device
cd "$device"        # Indexes into the directory on the computer
time="$(date)"      # The current date and time is set equal to the variable time
mkdir "$time"       # Makes a directory with the current date and time
cd "$_"     # Indexes into the directory with the date and time specified
adb pull /sdcard/BESI_C/        # Pulls the data from the specified directory in the device
cd ..       # Exits out one directory
cd ..       # Exits out one directory
echo "Successfully downloaded $device files"        # Prints a message if successful
done        # Exits the for loop and restarts

cd ..       # Exits out one directory

echo "Done with Extraction..."      # Message
echo "Exiting ..."      # Message
echo "Exiting BESI Download Script..."      # Message
echo "Leaving ADB Drivers: ACTIVE"      # Message
adb devices     # calls ADB devices again to show all the devices
echo "Returning to Home Directory..."       # Message

cd  $HOME       # Returns to home directory
