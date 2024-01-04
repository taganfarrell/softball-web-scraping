from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd


service = Service(executable_path='/Users/taganfarrell/PycharmProjects/datascrapingsoftball/chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open a webpage to test
driver.get("https://d1softball.com/statistics/")

print(driver.title)

# Get the list of years from the dropdown initially
year_dropdown = Select(driver.find_element(By.ID, 'main-stats-year'))
years = [option.text for option in year_dropdown.options]

for year in years:
    print(f"Processing year: {year}...")

    # Re-locate the dropdown and select the year for each iteration
    year_dropdown = Select(driver.find_element(By.ID, 'main-stats-year'))
    year_dropdown.select_by_visible_text(year)

    # Wait for the page to load the data for that year
    time.sleep(10)  # Adjust the sleep time as needed

    # After opening the page with driver.get, locate the dropdown
    # entries_dropdown = Select(driver.find_element(By.NAME, 'batting-stats_length'))
    entries_dropdown = Select(driver.find_element(By.NAME, 'pitching-stats_length'))

    # Select the 'All' option by its value
    entries_dropdown.select_by_value('-1')

    # Now wait for the page to load all entries before scraping
    time.sleep(5)  # Adjust the sleep time as necessary

    # Scrape the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the table with headers
    # table_headers = soup.find('table', class_='standard-batting-table')
    table_headers = soup.find('table', class_='standard-pitching-table')
    # Find the table with data rows
    table_data = soup.find('table', id='pitching-stats')

    # Initialize an empty list to store all the data
    data = []

    # Initialize an empty list to store header names
    headers = []

    # Check if the headers table is found
    if table_headers:
        print("Headers table found.")
        # Extract the table header names
        table_head = table_headers.find('thead')
        if table_head:
            headers = [th.get_text(strip=True) for th in table_head.find_all('th')]
            print("Headers extracted:", headers)
        else:
            print("Table header not found.")
    else:
        print("Headers table not found")

    # Check if the data table is found
    if table_data:
        print("Data table found.")
        # Extract the table data rows
        rows = table_data.find_all('tr')
        print(f"Found {len(rows)} rows in the data table.")

        # Iterate through the table rows
        for row in rows[1:]:  # skips first row of headers
            # Get all cells in the row
            cells = row.find_all('td')
            # Extract the text from each cell and add to the row data
            row_data = [cell.get_text(strip=True) for cell in cells]
            if row_data:
                print("Row data extracted:", row_data)
            else:
                print("Empty row encountered.")
            data.append(row_data)
    else:
        print("Data table not found.")

    # Convert the list of data into a pandas DataFrame, include headers
    df = pd.DataFrame(data, columns=headers)

    # Export the DataFrame to a CSV file with the year in its title
    # csv_path = f'/Users/taganfarrell/PycharmProjects/datascrapingsoftball/Batting_Data/ncaa_softball_batting_{year}.csv'
    csv_path = f'/Users/taganfarrell/PycharmProjects/datascrapingsoftball/Pitching_Data/ncaa_softball_pitching_{year}.csv'
    df.to_csv(csv_path, index=False)

    print(f"CSV file has been created for the year {year} at {csv_path}.")

print("closing browser")
# Close the browser when done
driver.quit()
