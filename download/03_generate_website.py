import datetime
import os
from datetime import datetime, timezone

from bs4 import BeautifulSoup

# Define the output directory
output_dir = '../out/'

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# List of supported image extensions
image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']

# Initialize lists to store image and HTML file paths
image_files = []
html_files = []

# Walk through the output directory and collect image and HTML files
for root, dirs, files in os.walk(output_dir):
    for file in files:
        if file.endswith('.html') and file != 'index.html':
            html_files.append(os.path.join(root, file))
        elif any(file.endswith(ext) for ext in image_extensions):
            image_files.append(os.path.join(root, file))

# Function to strip the hash from the file name
def strip_hash(file_name):
    parts = file_name.split('_')
    if len(parts) > 1:
        return '_'.join(parts[:-1]) + os.path.splitext(file_name)[1]
    return file_name

# Generate the HTML content with Bootstrap layout
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iShares Core MSCI World UCITS ETF, MSCI World Index Analysis</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="mt-4">iShares Core MSCI World UCITS ETF, MSCI World Index Analysis</h1>
        <h2 class="mt-4">Interactive Graphs</h2>
        <h5>☝️ After opening a graph, double click on a legend entry to focus on the corresponding entry! ☝️</h5>
        <ul class="list-group">
'''

for html_file in html_files:
    relative_path = os.path.relpath(html_file, output_dir)
    display_name = strip_hash(os.path.basename(relative_path))
    # if LARGE is in filename add a hint to the link text in brackets
    if 'LARGE' in display_name:
        display_name = display_name.replace('_LARGE', '') + ' (large file, takes some time to load!)'
    html_content += f'<li class="list-group-item"><a href="{relative_path}">{display_name}</a></li>'

html_content += '''
        </ul>
'''
        # <h2 class="mt-4">Image Files</h2>
        # <ul class="list-group">

# for image_file in image_files:
#     relative_path = os.path.relpath(image_file, output_dir)
#     display_name = strip_hash(os.path.basename(relative_path))
#     html_content += f'<li class="list-group-item"><a href="{relative_path}">{display_name}</a></li>'

        # </ul>
html_content += '''
    </div>
    <div class="mt-4 text-center">
        <img src="https://raw.githubusercontent.com/niesfisch/etf_index_analysis/refs/heads/main/doc/anim2.gif" alt="iShares Core MSCI World UCITS ETF Overview" width="800"/>
    </div>
    <div class="mt-4 text-center">last updated: ''' + str(datetime.now(timezone.utc).strftime('%Y-%m-%d %I:%M %p')) + ''' UTC</div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''

# Use BeautifulSoup to format the HTML content
soup = BeautifulSoup(html_content, 'html.parser')
formatted_html_content = soup.prettify()

# Save the formatted HTML content to a file
output_file = os.path.join(output_dir, 'index.html')
with open(output_file, 'w') as f:
    f.write(formatted_html_content)

print(f"Website generated and saved to {output_file}")