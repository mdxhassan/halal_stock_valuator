from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import numpy as np
import requests
import os 
from query import query_loop

api_key = os.getenv("API_KEY")

entries = 0

api_limit = 250
api_calls_made = 0

def next_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.find_element("xpath","/html/body/div/div[2]/div/div[3]/div[2]/div/ul/li[9]/a").click()
    time.sleep(2)  

def get_entries(table_body, max_entries, halal_only = False):
    global entries
    table_rows = table_body.find_elements(By.TAG_NAME, "tr")
    if halal_only:
        for row in table_rows:
            if entries >= max_entries:  # Stop if the maximum entries are reached
                print("MAX ENTRIES REACHED")
                break
            row_data = []
            table_data = row.find_elements(By.TAG_NAME, "td")
            
            # Extract data from each cell
            for data_cell in table_data:
                row_data.append(data_cell.text)
            
            # Check if the row has the expected number of columns (5 in this case)
            if len(row_data) == 5:
                if row_data[3] == "Comfortable":
                    cleaned_row_data = [item.replace(',', '') for item in row_data[:4]]
                    data.append(cleaned_row_data[:4])  # Append the first 4 columns only
                    entries += 1
                    print(f"Entry:{entries} has been added")
                else:
                    print(f"Skipping row without 'comfortable' in Halal status: {row_data[3]}")
    else:
        for row in table_rows:
            if entries >= max_entries:  # Stop if the maximum entries are reached
                print("MAX ENTRIES REACHED")
                break
            row_data = []
            table_data = row.find_elements(By.TAG_NAME, "td")
            for data_cell in table_data:
                row_data.append(data_cell.text)
            if len(row_data) == 5:  # Make sure row has the expected 4 columns
                cleaned_row_data = [item.replace(',', '') for item in row_data[:4]]
                data.append(cleaned_row_data[:4])  # Append the first 4 columns only
                entries += 1
                print(f"Entry:{entries} has been added")
    if halal_only:
        df_halal_only = pd.DataFrame(data, columns=["UID", "Company Name", "Ticker", "Halal Status"])
        return df_halal_only
    else:
        df = pd.DataFrame(data, columns=["UID", "Company Name", "Ticker", "Halal Status"])
        return df

def scrape_data(driver, max_pages, max_entries=5, halal_only=False):
    current_page = 0
    while current_page < max_pages and entries < max_entries:
        df = get_entries(table_body, max_entries, halal_only)
        current_page += 1
        next_page(driver)
    print ("Scraping Ended")
    driver.quit()
    return df

def get_financial_data(ticker, api_key, data_type):
    base_url = "https://financialmodelingprep.com/api"
    
    # Construct the URL based on the data type
    url = f"{base_url}/v3/{data_type}/{ticker}?apikey={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            # Extract data based on the type of request
            if data_type == "discounted-cash-flow":
                dcf_value = round(data[0].get("dcf"),2)
                price = data[0].get("price")
                return dcf_value
            
            elif data_type == "profile":
                description = data[0].get("description")
                industry = data[0].get("industry")
                sector = data[0].get("sector")
                price = data[0].get("price")
                return price, industry, sector, description
    
    return None, None

def classify_value(row):
    dcf_value = row['dcf_value']
    price = row['price']
    
    if pd.isna(dcf_value) or pd.isna(price):
        return "No data"
    
    if dcf_value > price * 1.05:  # 5% higher than price = undervalued
        return "Undervalued"
    elif dcf_value < price * 0.95:  # 5% lower than price = overvalued
        return "Overvalued"
    else:
        return "Correctly valued"
    
def add_api_details(df):
    global api_calls_made
    for index, row in df.iterrows():
        # Check if the API call limit has been reached
        if api_calls_made >= api_limit:
            print(f"API call limit of {api_limit} reached. No more API calls can be made.")
            break  # Stop processing once the rate limit is reached

        ticker = row['Ticker']

        try:
            # Fetch data from the API
            dcf_value = get_financial_data(ticker, api_key, "discounted-cash-flow")  
            price, industry, sector, description = get_financial_data(ticker, api_key, "profile")  

            # Increment the number of API calls after fetching data
            api_calls_made += 2  # Two API calls are made per ticker

            # Update the DataFrame with the new values, checking for None values
            if price is not None:
                df.at[index, 'Price'] = price
            if dcf_value is not None:
                df.at[index, 'DCF Value'] = dcf_value
            if industry is not None:
                df.at[index, 'Industry'] = industry
            if sector is not None:
                df.at[index, 'Sector'] = sector
            if description is not None:
                df.at[index, 'Description'] = description

            # Valuation logic
            if dcf_value and price:  # Ensure that both values exist
                if dcf_value > price * 1.05:  # 5% higher than price = undervalued
                    df.at[index, 'Valuation'] = "Undervalued"
                elif dcf_value < price * 0.95:  # 5% lower than price = overvalued
                    df.at[index, 'Valuation'] = "Overvalued"
                else:
                    df.at[index, 'Valuation'] = "Correctly valued"
            
            print(f"Successfully added API details for {ticker}")

        except Exception as e:
            # Print an error message and continue with the next row
            print(f"Error processing {ticker}: {e}")
            continue

def clean_dataframe(df):
    # Remove commas from all string columns
    df = df.replace(',', '', regex=True)
    # Drop rows with empty or NaN values
    df = df.dropna()
    # Remove duplicates
    df = df.drop_duplicates(inplace=True)

    return df

# Path to your webdriver
# Update this path to the location where you've installed your WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

#Open the page
url = "https://app.practicalislamicfinance.com/reports/stocks/"
driver.get(url)

# Give the page some time to load
time.sleep(2)

table_body = driver.find_element(By.TAG_NAME, "tbody")
number_of_pages = int(driver.find_element("xpath","/html/body/div/div[2]/div/div[3]/div[2]/div/ul/li[8]/a").text)
print(number_of_pages)

data = []

# Prompt user for max entries
while True:
    try:
        max_entries = int(input("Enter the max number of entries: "))
        if max_entries > 0:
            break
        else:
            print("Please enter a number greater than 0.")
    except ValueError:
        print("Please enter a valid integer.")

while True:
    try:
        halal_only = input("Do you want the database to only have halal stocks (Y/N): ")
        if halal_only.lower() == "y":
            halal_only = True
            break
        elif halal_only.lower() == "n":
            halal_only = False
            break
        else:
            print("Please enter a Y/N: ")
    except ValueError:
        print("Please enter a valid letter.")

# Call the scrape_data function with user input
df = scrape_data(driver, max_pages=number_of_pages, max_entries=max_entries, halal_only=halal_only)

#Saving scraped data
if halal_only:
    df.to_csv('halal_stocks_data.csv', index=False)
else:
    df.to_csv('stocks_data.csv', index=False) 

#Fill additional financial data from the API
add_api_details(df)

#Clean the dataframe
clean_dataframe(df)

# Save the data to a CSV file
if halal_only:
    df.to_csv('halal_stocks_valuation_data.csv', index=False)
else:
    df.to_csv('stocks_valuation_data.csv', index=False) 

#=== QUERY from Loaded Data ===#

while True:
    try:
        query = input("Do you want to ask questions about the data (Y/N): ")
        if query.lower() == "y":
            query_loop(df)
            break
            print("Program Ended")
        else:
            print("Program Ended")
            break
    except ValueError:
        print("Please enter a valid letter.")
   



#-----------------------------------------

# # Display the DataFrame (or use df.head() for a preview)
# print(df)
# df.to_csv('halal_stocks_data.csv', index=False)

# # Count how many rows have 'Halal Status' equal to "Comfortable"
# comfortable_count = np.sum(df['Halal Status'] == 'Comfortable')

# # Print the result
# print(f"Number of rows with Halal Status = 'Comfortable': {comfortable_count}")


# print ("PROGRAM ENDED")
# driver.quit()

#-----------------------------------

# # Extract the stock data
# stock_rows = driver.find_elements(By.CLASS_NAME, 'odd')

# data = []

# for row in stock_rows[1:]:  # Skipping the first row (header)
#     columns = row.find_elements(By.CSS_SELECTOR, 'td')
#     if len(columns) >= 4:
#         rank = columns[0].text
#         company_name = columns[1].text
#         ticker = columns[2].text
#         comfort_rating = columns[3].text
#         data.append([rank, company_name, ticker, comfort_rating])

# # Close the browser
# driver.quit()

# # Convert the data into a pandas DataFrame
# df = pd.DataFrame(data, columns=["Rank", "Company Name", "Ticker", "Comfort Rating"])

# # Display the data
# print(df)

# # Save the data to a CSV file
# df.to_csv('stocks_data.csv', index=False)


# for row in table_rows and entries <10:
#     row_data = []
#     table_data = row.find_elements(By.TAG_NAME, "td")
#     for data_cell in table_data:
#         row_data.append(data_cell.text)
#     if len(row_data) == 5 & c == 5:  # Make sure row has the expected 4 columns
#         data.append(row_data[:4])
#         entries += 1

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(10)
# driver.find_element("xpath","/html/body/div/div[2]/div/div[3]/div[2]/div/ul/li[9]/a").click()  
# print("NEXT PAGE")
# time.sleep(5)
# # Create a pandas DataFrame
# df = pd.DataFrame(data, columns=["UID", "Company Name", "Ticker", "Halal Status"])
