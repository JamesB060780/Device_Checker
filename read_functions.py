# imports
import pandas as pd

# read the files by filename
def read_files(device_file,user_file):
    device_df = pd.read_csv(device_file)
    user_df = pd.read_csv(user_file)

    return device_df, user_df

