import json
import os

# Create the data directory if it doesn't exist
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data')

# Delete all files in the data directory that are 16 bytes or smaller
for filename in os.listdir(data_dir):
    file_path = os.path.join(data_dir, filename)
    if os.path.isfile(file_path) and os.path.getsize(file_path) <= 16:
        print(f"Deleting {file_path} because it contains no data.")
        os.remove(file_path)

# Load and format all JSON files in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(data_dir, filename)
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)

        # Format the JSON data with indentation
        formatted_data = json.dumps(data, indent=4)

        # Write the formatted data back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_data)

        print(f"Formatted {file_path}")
