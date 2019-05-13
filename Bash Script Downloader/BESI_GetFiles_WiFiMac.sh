#!/usr/bin/env bash
echo    # Space
echo "---------------------------------------------------------------"   # Divider
echo    # Space

# MAC: Use this directory if you are on a mac $HOME
# WINDOWS: Use this directory if you are on a windows system /mnt/c/Users/inertia/Desktop

echo "!WELCOME!"       # Messages
echo "Running script at $(date)"   # Prints the time
echo    # Space
echo "Running System Commands"       # Messages
echo "Indexing to Specified Directory ..."       # Messages

cd $HOME       # Heads to the directory specified
cd Desktop        # Heads to the specified directory

mkdir "BESI-C-DATA"     # Makes a directory specified / checks if already made
cd "BESI-C-DATA"        # Indexes to the directory on the computer

echo "Waiting for Command ..."      # Message
echo "Running ADB Devices Command ..."       # Message

adb devices     # calls ADB devices again to show all the devices

FILE="$(adb devices)"       # Sets FILE to the command for ADB devices.
WatchIP0=192.168.60.100:5555       # This is a watch
WatchIP1=192.168.60.101:5555       # This is a watch
#WatchIP2=192.168.60.102:5555       # This is a watch
#WatchIP3=192.168.60.103:5555       # This is a watch
#WatchIP4=192.168.60.104:5555       # This is a watch
#WatchIP5=192.168.60.105:5555       # This is a watch
#WatchIP6=192.168.60.106:5555       # This is a watch
#WatchIP7=192.168.60.107:5555       # This is a watch
#WatchIP8=192.168.60.108:5555       # This is a watch
#WatchIP9=192.168.60.109:5555       # This is a watch
#WatchIP10=192.168.60.110:5555       # This is a watch

WATCHIP="$WatchIP0 ""$WatchIP1 ""$WatchIP2 ""$WatchIP3 ""$WatchIP4 ""$WatchIP5 ""$WatchIP6 ""$WatchIP7 ""$WatchIP8 ""$WatchIP9 ""$WatchIP10 "       # Possible watch IPs

echo    # Space
echo "Connecting to ADB Devices ..."       # Messages

for ip in $WATCHIP ; do     # For every device on the adb network
echo "Trying to connect to $ip ..."     # Message
adb connect $ip     # Try to connect to it
done        # Finish

echo    # Space
echo "$(adb devices)"       # Message
FILES="${FILE//List of devices attached/}"      # Removes the header from the output

echo    # Space

echo  "Rerunning connections to adb devices ..."       # Message to rerun the conneciton code

for ip in $WATCHIP ; do     # For every device on the adb network
echo "Trying to connect to $ip again ..."     # Message
adb connect $ip     # Try to connect to it again, to make sure
done        # Finish

echo    # Space
echo "$(adb devices)"       # Message
FILES="${FILE//List of devices attached/}"      # Removes the header from the output

echo    # Space
echo "Isolating Each IP_ADDRESS ..."        # Isolates the IP Address of the device
IP_ADDRESS_I="${FILES//device/}"       # Removes the device tag from the output of the device
IP_ADDRESS_II="${IP_ADDRESS_I//offline/}"       # Removes Offline in case device is offline
IP_ADDRESS_III="${IP_ADDRESS_II//unauthorized/}"       # Removes unauthorized in case device is not allowed
IP_ADDRESS_IV="${IP_ADDRESS_III//authorizing/}"       # Removes authorizing in case device is authorizing
IP_ADDRESS_FINAL="${IP_ADDRESS_IV//:5555/}"   # Removes the serial port from output of device
echo $IP_ADDRESS_FINAL     # Message

echo    # Space
echo "Running Data Collection Code..."      # Message

for device in $IP_ADDRESS_FINAL ; do        # For every device listed in adb devices
echo    # Space
echo "Device: $device"      # Message
echo "Reading Data from $device ..."       # Message
echo "Extracting Files from $device ..."        # Message

mkdir "$device"     # Makes a directory with the specified name
cd "$_"        # Indexes into the directory on the computer
time="$(date)"      # The current date and time is set equal to the variable time
mkdir "$time"       # Makes a directory with the current date and time
cd "$_"     # Indexes into the directory with the date and time specified
adb -s "$device:5555" pull /sdcard/BESI-C       # Pulls the data from the specified device
cd ..       # Exits out one directory
cd ..       # Exits out one directory
echo "Extracted and Saved $device files on $time"  # Prints a message;

done        # Exits the for loop and restarts

cd ..       # Exits out one directory

echo    # Space
echo "Done with Extraction..."      # Message
echo "Exiting ..."      # Message
echo "Exiting BESI Download Script..."      # Message

echo    # Space
echo "Leaving ADB Drivers: ACTIVE"      # Message
echo    # Space
adb devices     # calls ADB devices again to show all the devices

echo    # Space
echo "Returning to Home Directory..."       # Message

cd $HOME     # Goes to home directory
