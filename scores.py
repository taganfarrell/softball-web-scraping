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
driver.get("https://d1softball.com/team/abilchrist/")

# print(driver.title)

# Get the list of teams from the dropdown
teams_dropdown = Select(driver.find_element(By.NAME, 'teams'))
teams = [option.text for option in teams_dropdown.options]

# Get the list of years from the dropdown
year_dropdown = Select(driver.find_element(By.ID, 'team-season-select'))
years = [option.text for option in year_dropdown.options]

for year in years:
    print(f"Processing year: {year}...")
    # Initialize a list to hold all the rows of data
    data = []
    headers = ['Date', 'Home Team', 'Loc', 'Opponent', 'Score', 'Notes', 'Home Team Result']
    for team in teams[1:]:
        print(f"Processing team: {team}...")
        teams_dropdown = Select(driver.find_element(By.NAME, 'teams'))
        teams_dropdown.select_by_visible_text(team)
        year_dropdown = Select(driver.find_element(By.ID, 'team-season-select'))
        year_dropdown.select_by_visible_text(year)

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the div that contains the table
        team_schedule_div = soup.find('div', id='team-schedule')

        # Then find the table within that div
        table = None
        if team_schedule_div:
            table = team_schedule_div.find('table')
            if table:
                print("Table found.")
            else:
                print("Table not found within the div.")
        else:
            print("Div with id 'team-schedule' not found.")

        # Initialize an empty list to store header names
        headers2 = []

        if table:
            print("Table headers")
            # Extract the headers from the first row in the table header
            table_head = table.find('thead')
            if table_head:
                header_row = table_head.find('tr')
                if header_row:
                    headers2 = [td.get_text(strip=True) for td in header_row.find_all('td')]
                    headers2.append("Result")
                    print("Headers extracted:", headers2)
                else:
                    print("Header row not found.")
            else:
                print("Table headers not found.")

        # Extract the rows from the table body
        table_body = table.find('tbody')
        if table_body:
            print("Table body found")
            for row in table_body.find_all('tr'):
                # Initialize an empty list for this row's data
                row_data = []
                # Track the result separately
                result = ""
                is_home_game = False

                # check for home game
                cells_help = row.find_all('td')
                loc_text = cells_help[1].get_text(strip=True)  # Second cell for 'Loc'
                is_home_game = loc_text.lower() == 'vs'  # Check if it's a home game
                print("Home T/F = ", is_home_game)

                if is_home_game:
                    for cell in row.find_all('td'):
                        text = cell.get_text(strip=True)
                        text = text.replace('\xa0', ' ')  # Replace non-breaking spaces with regular spaces
                        print("text: ", text)
                        # Add the cell text to the row's data
                        row_data.append(text)
                        if 'class' in cell.attrs:
                            cell_classes = cell.attrs['class']
                            if 'result' in cell_classes:
                                result = 'Win' if 'win' in cell_classes else 'Loss' if 'lose' in cell_classes else ""

                    # Add the team name as 'Home Team'
                    row_data.insert(1, team)  # Assuming 'team' variable holds the home team name
                    # Append the result to the row's data
                    row_data.append(result)
                    # Remove the 'Win Prob' column data
                    win_prob_index = headers2.index('Win Prob') + 1
                    row_data.pop(win_prob_index)
                    # Append the row data to the data list
                    data.append(row_data)
                    print(f"row data: {row_data}")

    # Create a pandas DataFrame using the extracted data
    df = pd.DataFrame(data, columns=headers)

    # Print the DataFrame to verify
    # print(df)
    csv_path = f'/Users/taganfarrell/PycharmProjects/datascrapingsoftball/Game_Data/ncaa_game_results_{year}.csv'
    df.to_csv(csv_path, index=False)

    print(f"CSV file has been created for the year {year} at {csv_path}.")

print("closing browser")
# Close the browser when done
driver.quit()