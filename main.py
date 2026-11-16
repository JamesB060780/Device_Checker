# Imports
import pandas as pd
import datetime
import read_functions as func

# Get filename from user input
# filename = "windows_update_raw.csv"
filename = input("Enter the filename: ")

# Open and read file in dataframe - get agentid as the column index as unique
with open(filename) as file:
    device_df = pd.read_csv(file, index_col=0)

recent = []
current_OS = []
outstanding_updates = []
reboot_required = []
locations = []
# Loop through devices
for device in device_df.itertuples():
    # Check for recent usage (30 days)
    if datetime.datetime.fromisoformat(str(device.last_seen)) > (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)):
        recent.append(True)
    else:
        recent.append(False)

    # check for OS being current (windows 11 Pro)
    if "windows 11 pro" in str(device.operating_system).lower():
        current_OS.append(True)
    else:
        current_OS.append(False)

    # Check for Updates beyond Defender
    if int(str(device.pending_non_definition_unique_kb_count)) > 0:
        outstanding_updates.append(True)
    else:
        outstanding_updates.append(False)

    # Check for reboot requirement
    if str(device.needs_reboot).strip().lower() == "true":
        reboot_required.append(True)
    else:
        reboot_required.append(False)

    # Create locations list
    if str(device.site).strip() not in locations:
        locations.append(str(device.site).strip())

# Add to the dataframe
device_df['recent'] = recent
device_df['current_os'] = current_OS
device_df['outstanding_updates'] = outstanding_updates
device_df['reboot_required'] = reboot_required
# print(device_df.to_string())


# Give menu of locations
for i, location in enumerate(locations):
    print(f"{i + 1}. {location}")
location_choice = int(input("Enter the number of the location: ")) - 1

print("Select issue from the list:")
print("1. Unused")
print("2. Outdated OS")
print("3. Outstanding Updates")
print("4. Reboot Required")
print("5. All Issues")
issue_choice = int(input("Enter the number of the issue: ")) - 1

device_location_filtered = device_df[device_df['site'].str.strip() == locations[location_choice]]
if issue_choice == 0:  # Unused
    filtered = device_location_filtered[device_location_filtered['recent'] == False]
elif issue_choice == 1:  # Outdated OS
    filtered = device_location_filtered[device_location_filtered['current_os'] == False]
elif issue_choice == 2:  # Outstanding Updates
    filtered = device_location_filtered[device_location_filtered['outstanding_updates'] == True]
elif issue_choice == 3:  # Reboot Required
    filtered = device_location_filtered[device_location_filtered['reboot_required'] == True]
elif issue_choice == 4:  # All Issues
    filtered = device_location_filtered[
        (device_location_filtered['recent'] == False) |
        (device_location_filtered['current_os'] == False) |
        (device_location_filtered['outstanding_updates'] == True) |
        (device_location_filtered['reboot_required'] == True)
    ]
else:
    filtered = pd.DataFrame()  # Empty dataframe for invalid choice

if filtered.empty:
    print("No devices found for the selected criteria.")
else:
    # We need to print the filtered devices by computer name (hostname), the username and the OS,
    # if outstanding updates, if reboot required and when last seen
    # Print header for the filtered devices
    print()
    print(f"Here are the devices for {locations[location_choice]}")
    print(f"{'Hostname':<20} {'Username':<20} {'OS':<20} {'Outstanding Updates':<20} {'Reboot Required':<20} {'Last Seen':<20}")
    # Loop through the filtered devices and print their details
    for _, row in filtered.iterrows():
          print(
              f"{row['hostname']:<20} "
              f"{row['username']:<20} "
              f"{row['operating_system']:<20.14} "                      # Windows XX Pro
              f"{str(row['pending_non_definition_unique_kb_count']):<20} "
              f"{str(row['reboot_required']):<20} "
              f"{row['last_seen']:<20.10}"                              # Limited to just the date part of the string
            )
        