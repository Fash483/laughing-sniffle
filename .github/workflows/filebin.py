import os
import requests
import concurrent.futures

# Define the directory containing the files and the URL
directory = 'downloads'  # Folder containing files to upload
url_template = 'https://filebin.net/xx4gwonx76ay0bxu/{filename}'  # Use a placeholder for filename

# Function to upload a single file
def upload_file(file_path):
    filename = os.path.basename(file_path)  # Get the original filename
    url = url_template.format(filename=filename)  # Create the URL with the new filename

    with open(file_path, 'rb') as f:
        response = requests.post(url, headers={
            'accept': 'application/json',
            'Content-Type': 'application/octet-stream'
        }, data=f)  # Use data instead of files for binary upload
    
    return response.status_code, filename, response.json()  # Return status and response

# Gather all files in the specified directory
files_to_upload = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Use ThreadPoolExecutor to upload files concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Map the upload_file function to the list of files
    future_to_file = {executor.submit(upload_file, file): file for file in files_to_upload}
    
    for future in concurrent.futures.as_completed(future_to_file):
        try:
            status_code, filename, response_data = future.result()
            print(f'File: {filename}, Status Code: {status_code}, Response: {response_data}')
        except Exception as e:
            print(f'File: {future_to_file[future]} generated an exception: {e}')
