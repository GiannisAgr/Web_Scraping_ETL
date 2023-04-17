#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def get_fighters_df(url):
    
    '''
    Inputs a url from espn site of an mma athlete and returns a dataframe with statistics
    
    '''

    import numpy as np
    import pandas as pd
    import random
    import requests
    from bs4 import BeautifulSoup
    from time import sleep
    
    main_link = url.split('fighter')[0] + 'fighter/stats' + url.split('fighter')[1] # Starting point for each athlete
    headers = {'User-agent': ''}
    response = requests.get(main_link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    sleep(3 + random.random())

    # If this table exists get all those below
    if soup.find('div', class_='ResponsiveTable pt4'):

        try: name = ' '.join([span.text for span in soup.find('h1', {'class': 'PlayerHeader__Name'}).find_all('span')])
        except: name = np.nan

        try: country = soup.find('li', class_='truncate min-w-0').text
        except: country = np.nan

        try: division = soup.find('li', class_='').text
        except: division = np.nan

        try: height = soup.find('div', class_='ttu', text='HT/WT').find_next_sibling('div').text.split(',')[0] # Height
        except: height = np.nan

        try: weight = soup.find('div', class_='ttu', text='HT/WT').find_next_sibling('div').text.split(',')[1] # Weight
        except: weight = np.nan

        try: birth_date = soup.find('div', class_='ttu', text='Birthdate').find_next_sibling('div').text # Birth date
        except: birth_date = np.nan

        try: team = soup.find('div', class_='ttu', text='Team').find_next_sibling('div').text # Team
        except: team = np.nan

        try: stance = soup.find('div', class_='ttu', text='Stance').find_next_sibling('div').text # Stance
        except: stance = np.nan

        try: reach = soup.find('div', class_='ttu', text='Reach').find_next_sibling('div').text # Reach
        except: reach = np.nan



        try: wins_loses_draws = soup.find('div', attrs={"aria-label": "Wins-Losses-Draws"}).find_next_sibling('div').text # W-L-D
        except: wins_loses_draws = np.nan

        try: ko_tko_wins = soup.find("div", attrs={"aria-label": "Technical Knockout-Technical Knockout Losses"}).find_next_sibling("div").text.split('-')[0] # (T)KO wins
        except: ko_tko_wins = np.nan

        try: ko_tko_loses = soup.find("div", attrs={"aria-label": "Technical Knockout-Technical Knockout Losses"}).find_next_sibling("div").text.split('-')[0] # (T)KO loses
        except: ko_tko_loses = np.nan

        try: submission_wins = soup.find("div", attrs={"aria-label": "Submissions-Submission Losses"}).find_next_sibling("div").text.split('-')[0] # Submission wins 
        except: submission_wins = np.nan

        try: submission_loses = soup.find("div", attrs={"aria-label": "Submissions-Submission Losses"}).find_next_sibling("div").text.split('-')[1] # Submission loses
        except:  submission_loses = np.nan




        try:
            # Find the striking table if it exists
            striking_table = soup.select_one(".ResponsiveTable:-soup-contains('striking') table")

            # If its not empty
            if striking_table:
                # Extract the headers of the table
                headers_striking = [th.text.strip() for th in striking_table.select("thead th")]

                # Extract the rows of the table
                rows_striking = []
                for tr in striking_table.select("tbody tr"):
                    cells_striking = [td.text.strip() for td in tr.select("td")]
                    rows_striking.append(cells_striking)
        except:
            pass

        try:
            # Find the clinch table if it exists
            clinch_table = soup.select_one(".ResponsiveTable:-soup-contains('Clinch') table")

            # If its not empty
            if clinch_table:
                # Extract the headers of the table
                headers_clinch = [th.text.strip() for th in clinch_table.select("thead th")]

                # Extract the rows of the table
                rows_clinch = []
                for tr in clinch_table.select("tbody tr"):
                    cells_clinch = [td.text.strip() for td in tr.select("td")]
                    rows_clinch.append(cells_clinch)
        except:
            pass

        try:
            # Find the ground table if it exists
            ground_table = soup.select_one(".ResponsiveTable:-soup-contains('Ground') table")

            # If its not empty
            if ground_table:
                # Extract the headers of the table
                headers_ground = [th.text.strip() for th in ground_table.select("thead th")]

                # Extract the rows of the table
                rows_ground = []
                for tr in ground_table.select("tbody tr"):
                    cells_ground = [td.text.strip() for td in tr.select("td")]
                    rows_ground.append(cells_ground)
        except:
            pass

        # Go to fight history page
        main_link = url.split('fighter')[0] + 'fighter/history' + url.split('fighter')[1]
        headers = {'User-agent': ''}
        response = requests.get(main_link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        sleep(3 + random.random())

        try:
            # Find the fight history table if it exists
            fight_history_table = soup.select_one(".ResponsiveTable:-soup-contains('Fight') table")

            # If its not empty
            if fight_history_table:
                # Extract the headers of the table
                headers_fight_history = [th.text.strip() for th in fight_history_table.select("thead th")]

                # Extract the rows of the table
                rows_fight_history = []
                for tr in fight_history_table.select("tbody tr"):
                    cells_fight_history = [td.text.strip() for td in tr.select("td")]
                    rows_fight_history.append(cells_fight_history)
        except:
            pass    



        '''
        Finally we make 3 dataframes and then combine them to 1
        
        '''
        
        try:
            # Dataframe of the striking, clinch, ground tables with columns names the headers which we extracted
            temp_tables = pd.DataFrame(rows_striking, columns=headers_striking).merge(
                              pd.DataFrame(rows_clinch, columns=headers_clinch), on=['Date', 'Opponent', 'Event', 'Res.']).merge(
                                  pd.DataFrame(rows_ground, columns=headers_ground), on=['Date', 'Opponent', 'Event', 'Res.'])

            # Dataframe of name country etc.. (these values wont change for each fighter)
            temp_stats = pd.DataFrame([[name, country, division, height, weight, birth_date, stance, reach]] * len(temp_tables),
                              columns=['name', 'country', 'division', 'height', 'weight', 'birth_date', 'stance', 'reach'])

            # Dataframe of fight history
            temp_fight_history = pd.DataFrame(rows_fight_history, columns=headers_fight_history)
            # Exclude the EVENT column
            temp_fight_history = temp_fight_history.loc[:, temp_fight_history.columns != 'Event']

            # Combine 3 dataframes to 1
            df= temp_stats.merge(
                    temp_tables.merge(
                        temp_fight_history, on=['Date', 'Opponent', 'Res.']), left_index=True, right_index=True)
            return df

        except:
            pass   


def fixing_collumns(col, col_to_fix, df):
    
    '''
    Inputs a column and a column to fix ('_x', '_y' etc..).
    If a value of the column to fix is not null leave it as it is, else replace it with the value of the proper column
    Outputs the updated column (pandas Series)
    
    '''

    import numpy as np
    
    try:
        df[col] = np.where(df[col_to_fix].notnull(), df[col_to_fix], df[col])    
    except:
        pass
    
    return df[col]




def get_stats_ufc(link):
    
    '''
    Inputs a url for a fighter in the ufc page.
    Outputs a dataframe with statistics.
    
    '''

    import numpy as np
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    from time import sleep
    import random
    
    
    main_link = link
    headers = {'User-agent': ''}
    response = requests.get(main_link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    sleep(3 + random.random())
    
    
    try: name = ' '.join(main_link.split('/')[-1].split('-')).title()
    except: name = np.nan

    try: hometown = soup.find('div', class_='c-bio__label', text='Hometown').find_next_sibling('div', class_='c-bio__text').text # Hometown
    except: hometown = np.nan

    try: fighting_style = soup.find('div', class_='c-bio__label', text='Fighting style').find_next_sibling('div', class_='c-bio__text').text # Style
    except: fighting_style = np.nan

    try: height = soup.find('div', class_='c-bio__label', text='Height').find_next_sibling('div', class_='c-bio__text').text # Height
    except: height = np.nan

    try: weight = soup.find('div', class_='c-bio__label', text='Weight').find_next_sibling('div', class_='c-bio__text').text # Weight
    except: weight = np.nan

    try: reach = soup.find('div', class_='c-bio__label', text='Reach').find_next_sibling('div', class_='c-bio__text').text # Reach
    except: reach = np.nan

    try: leg_reach = soup.find('div', class_='c-bio__label', text='Leg reach').find_next_sibling('div', class_='c-bio__text').text # Reach
    except: leg_reach = np.nan
        
        
    df = pd.DataFrame([[name, hometown, fighting_style, height, weight, reach, leg_reach]],
                              columns=['name', 'hometown', 'fighting_style', 'height', 'weight', 'reach', 'leg_reach'])
    
    return df




def get_stats_ufcstats(link):
    
    '''
    Inputs a url for a fighter in the ufcstats page.
    Outputs a dataframe with statistics.
    
    '''
    import numpy as np
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    from time import sleep
    import random
        
    main_link = link
    headers = {'User-agent': ''}
    response = requests.get(main_link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    sleep(3 + random.random()) # they are too many to give a bigger sleep

    try: name = soup.find('span', class_='b-content__title-highlight').text.strip() # Name
    except: name = np.nan

    try: height = soup.select_one("li:-soup-contains('Height')").text.replace("Height:", "").strip()
    except: height = np.nan

    try: weight = soup.select_one("li:-soup-contains('Weight')").text.replace("Weight:", "").strip()
    except: weight = np.nan

    try: reach = soup.select_one("li:-soup-contains('Reach')").text.replace("Reach:", "").strip()
    except: reach = np.nan

    try: stance = soup.select_one("li:-soup-contains('STANCE')").text.replace("STANCE:", "").strip()
    except: stance = np.nan

    try: date_of_birth = soup.select_one("li:-soup-contains('DOB')").text.replace("DOB:", "").strip()
    except: date_of_birth = np.nan
        
    df = pd.DataFrame([[name, height, weight, reach, stance, date_of_birth]],
                              columns=['name', 'height', 'weight', 'reach', 'stance', 'date_of_birth'])
    
    return df




def insert_data(cur, data, values):
    
    '''
    Insert data to the table in our database
    
    '''
    
    # Define the SQL statement for inserting data into a table
    insert_query = f"""
    INSERT INTO mma (
        ID,
        name,
        country,
        division,
        height,
        weight,
        birth_date,
        stance,
        reach,
        Date,
        Opponent,
        Event,
        Res,
        SDBL_A,
        SDHL_A,
        SDLL_A,
        TSL,
        TSA,
        SSL,
        SSA,
        TSL_TSA_percent,
        KD,
        BODY_percent,
        HEAD_percent,
        LEG_percent,
        SCBL,
        SCBA,
        SCHL,
        SCHA,
        SCLL,
        SCLA,
        RV,
        SR,
        TDL,
        TDA,
        TDS,
        TK_ACC_percent,
        SGBL,
        SGBA,
        SGHL,
        SGHA,
        SGLL,
        SGLA,
        AD,
        ADTB,
        ADHG,
        ADTM,
        ADTS,
        SM,
        Decision,
        Rnd,
        Time,
        hometown,
        fighting_style,
        leg_reach,
        SDBL,
        SDBA,
        SDHL,
        SDHA,
        SDLL,
        SDLA)
    VALUES ({values});
    """

    # Execute the SQL statement to insert data into the table
    cur.executemany(insert_query, data)