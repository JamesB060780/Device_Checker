# Checking and mapping PC requirements
The goal is to identify problem PCs before arriving on site. It makes use of the technician/engineer's time while on site to ensure smooth operation of all devices and awareness of problems before they arise. 

## Download the csv file from the RMM
The user downloads the csv using the RMM software. This has some key metrics, which need to be used by the software to narrow down individual issues and PCs. These are to find simple problems which can be fixed, or flag devices for disposal. 

## Select file
The file is read in as a string input. 

## Select location
The user selects the location they are either at or arriving on. The focus is just on these, as we cover multiple sites and various locations. 

## Problems
The user might just want to reboot specific PCs, or check the windows update function. This helps to reduce the number of devices the technician is focussing on, making maximum use of their time. For example, I travelled to Milton Keynes and wanted to ensure all updates were completed. I was already disposing of a PC, and there was already a plan for the next one. I wanted to know whose PC I needed to check for the updates and why they are stalling. 

## Running
Use python to run main.py. It will request the necessary details
