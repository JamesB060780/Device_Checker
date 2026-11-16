# Imports
import pandas as pd
import my_functions as func

# Get filename from user input
filename = input("Enter the filename: ")

# Open and read file in dataframe - get agentid as the column index as unique
with open(filename) as file:
    device_df = pd.read_csv(file, index_col=0)

# Call function to create the extra columns for filter, and the locations list
device_df, locations = func.create_columns(device_df)

# Give menu of locations - remember zero index adjustment
for i, location in enumerate(locations):
    print(f"{i + 1}. {location}")
location_choice = int(input("Enter the number of the location: ")) - 1

print("Select issue from the list:")
print("1. Unused")
print("2. Outdated OS")
print("3. Outstanding Updates")
print("4. Reboot Required")
print("5. All Issues")
issue_choice = int(input("Enter the number of the issue: "))

device_location_filtered = device_df[
    device_df['site'].str.strip() == locations[location_choice]
]

if issue_choice == 1:  # Unused - "~" is "not" operator for boolean
    filtered = device_location_filtered[~device_location_filtered['recent']]
elif issue_choice == 2:  # Outdated OS
    filtered = device_location_filtered[~device_location_filtered['current_os']]
elif issue_choice == 3:  # Outstanding Updates
    filtered = device_location_filtered[device_location_filtered['outstanding_updates']]
elif issue_choice == 4:  # Reboot Required
    filtered = device_location_filtered[device_location_filtered['reboot_required']]
elif issue_choice == 5:  # All Issues
    # Use "|" as OR to combine statements
    filtered = device_location_filtered[
        (~device_location_filtered['recent']) |
        (~device_location_filtered['current_os']) |
        (device_location_filtered['outstanding_updates']) |
        (device_location_filtered['reboot_required'])
    ]
else:
    filtered = pd.DataFrame()  # Empty dataframe for invalid choice

if filtered.empty:
    print("No devices found for the selected criteria.")
else:
    # Print the filtered devices
    func.print_filtered_devices(filtered, locations[location_choice])