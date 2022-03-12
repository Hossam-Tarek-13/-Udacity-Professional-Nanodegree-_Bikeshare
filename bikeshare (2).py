import time
import pandas as pd
import numpy as np
import inquirer

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    

    while True:
        city = input("Please enter desired city: \n ch for chicago \n ny for new york city \n wa for washington \n ").lower()
        if city =='chicago' or city == 'ch':
            city = 'chicago'
                
            break
                
        elif city =='new york city' or city =='ny':
            city = 'new york city'
                
            break
                
        elif city =='washington' or city == 'wa':
            city ='washington'
                
            break
                
        else:
            print("\nSorry, Invalid input.\nPlease try again \n")
                
            continue          

    questions = [
    inquirer.List('month',
                message="Please select desired month filter",
                choices=['all', 'january', 'february', 'march', 'april', 'may', 'june'],
            ),
    ]
    month_dict = inquirer.prompt(questions) 
    month = list(month_dict.values())[0]
    

    
    questions = [
    inquirer.List('day',
                message="Please select desired month filter",
                choices=['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'],
            ),
    ]
    day_dict = inquirer.prompt(questions)
    day = list(day_dict.values())[0]


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month!='all':
        #use the index of the month list to get the corresponding int
        months=['january','february','march','april','may','june']
        month=months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
 
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month                    
    common_month = df['month'].mode()[0]
    print("Most common month= ", common_month)

    # TO DO: display the most common day of week
    common_day = df['day'].mode()[0]
    print("Most common day= ", common_day)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print("Most common hour= ", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("Popular Start:\n", common_start)

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("Popular End:\n", common_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['combination'].mode()[0]
    print("Common Trip:\n", common_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print("Total trip duration adds up to:\n", total_trip_duration)

    # TO DO: display mean travel time
    average_trip_duration = df['Trip Duration'].mean()
    print("Average trip duration adds up to:\n", average_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
       
    print("Count of users:\n", df['User Type'].value_counts())
   
    
    # TO DO: Display counts of gender
    if 'Gender' in df:
        print("Count of gender:\n", df['Gender'].value_counts())
    else:
        print('Sorry, It is a desert here')  


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = df['Birth Year'].min()
        print("Earliest year of birth:", int(earliest))
        recent = df['Birth Year'].max()
        print("Most recent year of birth:", int(recent))
        common_birth = df['Birth Year'].mode()[0]
        print("Most common year of birth:", int(common_birth))
        
    else:
        print("There is no birth year information in this city.\n")
     
    raw_data = 0
    while True:
        answer = input("Do you want to have a peek into the raw data? [y/n]\n").lower()
        if answer not in ['y', 'n']:
            answer = input("You wrote the wrong word. Please type y or n.\n").lower()
        elif answer == 'y':
            raw_data += 5
            print(df.iloc[raw_data : raw_data + 5])
        elif answer == 'n':
            break
        again = input("Do you want to see more? [y/n]\n").lower()
        if again not in ['y', 'n']:
            again = input("You wrote the wrong word. Please type y or n.\n").lower()        
        elif again == 'n':
            break
        elif answer == 'n':
            return

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
