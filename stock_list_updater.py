import requests
import pandas as pd
from io import StringIO

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1hX501C2zCJxNBrNw3ZhRmKgi3YmEGtajMSTUmPcXuDkVDVh5TZ9ZAVr8MsYJ3YC-SOpIicOfmtn5/pub?gid=0&single=true&output=csv"
# Download the CSV file content
response = requests.get(sheet_url)

# Check if the request was successful
if response.status_code == 200:
    # Convert the CSV content to a Pandas DataFrame
    data = StringIO(response.text)
    stock_data = pd.read_csv(data)
    
    # Display the first few rows of the data
    print('updated list data recieved')
    stock_data.to_csv('Stock_list.csv', index=False)
    print('list updated')
else:
    print(f"Failed to download the file, status code: {response.status_code}")

