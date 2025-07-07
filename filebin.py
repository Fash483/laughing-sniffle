import os
import subprocess

# Define the directory and Filebin URL template
directory = 'downloads'
url_template = 'https://filebin.net/wrjtapwqd8l93y8u/{filename}'

# Function to URL-encode the file path and filename
def encode_filename(filename):
    return filename.replace(' ', '%20').replace('(', '%28').replace(')', '%29')

# Iterate through all files in the directory and subdirectories
for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        # Get the filename and URL encode it
        encoded_filename = encode_filename(file)
        url = url_template.format(filename=encoded_filename)

        # Use subprocess to call curl command for each file
        print(f"Uploading {file}...")
        result = subprocess.run(
            ['curl', '--globoff', '-X', 'POST', '-H', 'Content-Type: application/octet-stream', '--data-binary', f'@{file_path}', url],
            capture_output=True, text=True
        )

        # Print result of upload
        print(f"Upload result for {file}: {result.stdout}")
        if result.stderr:
            print(f"Error uploading {file}: {result.stderr}")
