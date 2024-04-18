import pandas as pd
import json
import os

def json_to_csv(filepath, output_file_path):
# Read the JSON file
    with open(filepath, "r") as f:
      json_data = json.load(f)
    # Convert JSON data to a pandas DataFrame
    df = pd.DataFrame(json_data)
    for index, row in df.iterrows():
        if row['thresh'] == '1':
            start_index = max(0, index - 50)
            df.loc[start_index:index, 'label'] = row['label']
    # I don't know why, but it breaks if I remove this...
    df.to_csv("Temp/temp_LSTM.csv")
    df = pd.read_csv("Temp/temp_LSTM.csv",index_col=0)
    try:
        df['coordinates'] = df['coordinates'].apply(lambda x: list(map(int, x.strip("[]").replace("'", "").split(','))))
    except Exception as e:
        print(f"Error converting coordinates: {e}")
        return

    # Remove rows where the 'coordinate' list has less than 7 values
    df = df[df['coordinates'].apply(len) == 7]
    df.dropna(inplace=True)

    # Save the processed DataFrame as a new CSV file
    df.to_csv(output_file_path, index=False)

    print(f"Processed data saved as {output_file_path}")

def get_file_names(directory):
    return os.listdir(directory)

def combine_csv_files(directory, output_file):
    size = 50
    # Get a list of all CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the directory.")
        return
    # Initialize an empty DataFrame
    df_combined = pd.DataFrame()
    # Loop through the list of CSV files and read each one into a DataFrame
    for file in csv_files:
        df = pd.read_csv(os.path.join(directory, file))
        if 'thresh' not in df.columns:
            print(f"The file {file} does not have a 'thresh' column.")
            continue
        df_combined = pd.concat([df_combined, df])
    df_combined.reset_index(drop=True, inplace=True)
    df_combined.to_csv(output_file)

i = 0
for file_paths in get_file_names('./Training sets'):
    json_to_csv(f"./Training sets/{file_paths}", f"./Raw_csvs/formatted_{str(i)}.csv")
    i += 1
combine_csv_files('./Raw_csvs','frames.csv')
