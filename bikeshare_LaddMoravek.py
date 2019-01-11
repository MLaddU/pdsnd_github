import time
import csv
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data! This will be exciting')
    
    # get user input for city (chicago, new york city, washington)
    
    city_correct = False
    city_list = ['chicago', 'new york city', 'washington']
    while city_correct == False:
            print('Which city\'s data do you want to see?')
            city_input = str(input('Please enter New York City, Chicago, or Washington: ' ))
            city = ' '.join(city_input.lower().split())
            if city in city_list:
                print('You selected {}'.format(city.title()))
                city_correct = True
            else:
                print('Oops! That is not a valid city name!')
                print('Please enter either New York City, Chicago, or Washington AND check your spelling!')
  


    # get user input for month (all, january, february, ... , june)
    
    month_correct = False
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month_correct == False:
            print('Which month\'s data do you want to see?')
            month_input = str(input('Please enter January, February, March, April, May, June, or All: ' ))
            month = month_input.lower()
            if month in month_list:
                print('You selected {}'.format(month.title()))
                month_correct = True
            else:
                print('That is not a valid month name!')
                print('Please enter either January, February, March, April, May, June, or All AND check your spelling!')



    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    day_correct = False
    day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day_correct == False:
            print('Which day of the week\'s data do you want to see?')
            day_input = str(input('Please enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All: ' ))
            day = day_input.lower()
            if day in day_list:
                print('You selected {}'.format(day.title()))
                day_correct = True
            else:
                print('That is not a valid day of the week name!')
                print('Please enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All AND check your spelling!')

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
    # load data file into a dataframe
    
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime fields (i.e. month and day of week)
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        df = df[df['month'] == month]

    # filter by day of week if applicable
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = df['month'].mode()[0]
    print('Most Popular Month: ', months[popular_month-1].title())

    # display the most common day of week
    
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of the Week: ', popular_day)
    
    # display the most common start hour
    
    popular_hour = df['start_hour'].mode()[0]
    print('Most Popular Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Sation: ', popular_start_station)

    # display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Sation: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    
    station_combination = df['Start Station'] + ' -AND- ' + df['End Station']
    popular_station_combination = station_combination.mode()[0]
    print('Most Popular Start and End Station Combination: ', popular_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time (in hours): ',round(sum(df['Trip Duration'])/3600, 2))

    # display mean travel time
    print('Mean Travel Time (in minutes): ',round(np.mean(df['Trip Duration'])/60, 2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #df['User Type'].fillna('None')
    print('Counts of User Types:')
    print(df['User Type'].value_counts())
    print('\n')

    # Display counts of gender

    if city != 'washington': 
        print('Counts of Gender Types:')
        print(df['Gender'].value_counts())
        print('\n')
    else:
        print('Washington does not provide data for gender.')
        print('\n')
    
    # Display earliest, most recent, and most common year of birth

    if city != 'washington':
        print('User Year of Birth Stats:')
        print('Earliest Year of Birth: ',int(df['Birth Year'].min()))
        print('Most Recent Year of Birth: ',int(df['Birth Year'].max()))
        common_birth_year = df['Birth Year'].mode()[0]
        print('Most Common Year of Birth: ',int(common_birth_year))
        print('\n')
    else:
        print('Washington does not provide data for year of birth.')
        print('\n')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def read_for_user():
    """Displays 5 rows of raw dat from the .csv file."""
    
    start_row=0
    read_rows=5
    
    # get input to determine if user wants to see raw data 
    
    data_input = input('Do you want to see the raw data (5 lines at a time)? Enter yes or no.\n' )
    while data_input.lower() != 'yes' and data_input.lower() != 'no':
        print('Please enter either yes or no')
        data_input = input('Do you want to see the raw data (5 lines at a time)? Enter yes or no.\n' )
    while data_input.lower() == 'yes':
        with open(CITY_DATA[city],'r') as raw_file:
            read = csv.reader(raw_file)
            for i in range(start_row):
                next(read)
            for i in range(read_rows):
                print(next(read))
            start_row += 5
            print('\n')
            data_input = input('Do you want to see more raw data (5 lines at a time)? Enter yes or no.\n' )
            while data_input.lower() != 'yes' and data_input.lower() != 'no':
                print('Please enter either yes or no')
                data_input = input('Do you want to see the raw data (5 lines at a time)? Enter yes or no.\n' )
            print('\n')

    

"""
Main block of code
"""
if __name__ == "__main__":
    restart = 'yes'
    while restart.lower() == 'yes':
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        read_for_user()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() != 'yes' and restart.lower() != 'no':
            print('Please enter either yes or no')
            restart = input('\nWould you like to restart? Enter yes or no.\n')