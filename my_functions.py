import datetime

def create_columns(device_df):
    recent = []
    current_OS = []
    outstanding_updates = []
    reboot_required = []
    locations = []

    # Find cut off date - avoid calculating through loop for each device
    cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)

    for device in device_df.itertuples():
    # Check for recent usage (30 days)
        if datetime.datetime.fromisoformat(str(device.last_seen)) > cutoff_date:
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

    # Returns new dataframe with the locations
    return device_df, locations

def print_filtered_devices(filtered, location):
    print()
    print(f"Here are the devices for {location}")

    # Print header for the filtered devices
    print(
        f"{'Hostname':<20} "
        f"{'Username':<20} "
        f"{'OS':<20} "
        f"{'Outstanding Updates':<20} "
        f"{'Reboot Required':<20} "
        f"{'Last Seen':<20}"
    )

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
        