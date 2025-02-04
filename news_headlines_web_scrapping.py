import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Step 1: Define the target URL
url = "https://www.bbc.com/news"

# Step 2: Send a request to fetch the page content
response = requests.get(url)
if response.status_code == 200:  # Check if the request was successful
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Step 3: Extract headlines
    headlines = soup.find_all("h3")  # Finding all <h3> elements

    # Step 4: Prepare data for storage
    data = []
    for index, headline in enumerate(headlines[:10]):  # Limiting to top 10 headlines
        text = headline.get_text(strip=True)  # Extract text
        data.append({"Index": index + 1, "Headline": text, "Timestamp": datetime.now()})

    # Step 5: Convert to DataFrame
    df = pd.DataFrame(data)

    # Step 6: Save to CSV file (append mode)
    csv_filename = "news_headlines.csv"
    
    try:
        existing_df = pd.read_csv(csv_filename, on_bad_lines='skip')
        df.to_csv(csv_filename, mode='a', index=False, header=False)
    except FileNotFoundError:
        df.to_csv(csv_filename, mode='w', index=False, header=True)

    print(f"Scraped {len(data)} headlines and saved to {csv_filename}")
else:
    print("Failed to retrieve the web page.")
