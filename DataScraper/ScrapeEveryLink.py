import pandas as pd
import DataScraper

# Scrapes every link
# Before running this file you must run linkscraper.py at least once
# This file runs through every link and creates the game data csv file
# entire_data_scraper() runs through every link in the game_links.csv file generated by linkscraper.py and returns a brand new dataframe with new scraped data for every link into the complete_game_data.csv file
# The progress_game_data.csv file allows the user to watch the progress of the entire_data_scraper() function as it runs

# Scrape the data for every link in the game_links.csv
def entire_data_scraper():
    # Read the game_links.csv file
    game_link_df = pd.read_csv('../game_links.csv')

    # Manually order the columns
    df_header = ['Name', 'Platform', 'MSRP', 'Buy Digital', 'Buy Physical', 'Demo Available', 'DLC Available', 'Publisher', 'Developer', 'ESRB', 'Release Date', 'No. of Players', 'Rom File Size', 'Switch Online Play', 'Switch Online Save', 'Switch Online App']
    category_name_list = sorted(DataScraper.category_parser())
    df_header.extend(category_name_list)
    df_header.extend(['Store Link', 'Official Site', 'Time Data Retrieved (UTC)'])
    
    # Create the list of dictionaries of all the game data
    data_dictionary = []
    for platform in game_link_df:
        # Drop the NaN values of the dataframe
        game_links = game_link_df[platform].dropna()
        num_links = game_links.size
        sum = 1
        for url in game_links:
            # Print the link number being processed
            print('\n \n')
            print(platform, ': Processing link #', sum, 'out of', num_links)
            # Set the link data dictionary to the data scraper results
            link_data_dict = DataScraper.page_parser(url, category_name_list)
            attempts = 1
            # If the Name column is ERROR, repeat the attempt to scrape the site up to 10 times
            while link_data_dict['Name'] == 'ERROR' and attempts <= 10:
                print("ATTEMPT: ", attempts)
                attempts += 1
                link_data_dict = DataScraper.page_parser(url, category_name_list)

            if attempts == 11:
                print('ERROR, failed but appended')
            else:
                pass

            # Every 100 links update the progress_game_data.csv file with an updated dataframe
            data_dictionary.append(link_data_dict)
            if sum % 100 == 0:
                data_df = pd.DataFrame.from_dict(data_dictionary)
                ordered_data_df = data_df[df_header]
                ordered_data_df.to_csv('../progress_game_data.csv', index=False)
                print('---UPDATED progress_game_data.csv---')
            else:
                pass
            sum += 1
        # Every time all platform links are finished being scraped, update the progress_game_data.csv with an updated dataframe
        data_df = pd.DataFrame.from_dict(data_dictionary)
        ordered_data_df = data_df[df_header]
        ordered_data_df.to_csv('../progress_game_data.csv', index=False)
        print('---UPDATED progress_game_data.csv---')

    # Update the final_game_data.csv with the finished scraped data
    data_df = pd.DataFrame.from_dict(data_dictionary)
    ordered_data_df = data_df[df_header]
    ordered_data_df.to_csv('../complete_game_data.csv', index=False)
    print('---FINAL UPDATE complete_game_data.csv---')


entire_data_scraper()