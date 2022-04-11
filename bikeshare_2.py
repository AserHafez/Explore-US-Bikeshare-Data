import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv' }

def check_data_entry(prompt, valid_entries): 
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()

        while user_input not in valid_entries : 
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        print('Great! the chosen entry is: {}\n'.format(user_input).title())
        return user_input

    except:
        print('Seems like there is an issue with your input')



def get_filters(): 
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hi there! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Please choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)


    # get user input for month (all, january, february, ... , june)
    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Would you like to filter by month?\nif "Yes"...please type a month name from January to June.\nif "No"....please type "ALL" for no filter.\n'
    month = check_data_entry(prompt_month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Would you like to filter by day?\nif "Yes"...please type Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.\nif "No"....please type "ALL" for no filter.\n'
    day = check_data_entry(prompt_day, valid_days)


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
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
        month = months[month]
    
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]
    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    
    most_common_month = df['Month'].value_counts().index[0]
    
    datetime_object = datetime.datetime.strptime(str(most_common_month), "%m")
    month_name = datetime_object.strftime("%B")
    
    print('The Most Common Month is: ', month_name)
    
    # display the most common day of week
    
    most_common_day = df['Day of Week'].value_counts().index[0]
    print('The Most Common Day is: ', most_common_day)

    # display the most common start hour
    most_comon_start_hour = pd.to_datetime(df['Start Time']).dt.hour.value_counts().index[0]
    print('The Most Common hour is: ', most_comon_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().index[0]
    print('The Most Common Start Station is:\n', most_common_start_station, '.')

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().index[0]
    print('The Most Common End Station is:\n', most_common_end_station, '.')

    # display most frequent combination of start station and end station trip
    most_freq_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most Frequent Combination of Start and End Station Trip is: ', most_freq_combination, '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    #total_travel_time_conv = str(datetime.timedelta(seconds=df['Trip Duration'].sum())
    print('Total Trip Duration: ', total_travel_time, 'seconds.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time: ', mean_travel_time, 'seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
        
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('User Types Counts:\n',user_types_count)

    # Display counts of gender
    if 'Gender' not in df:
        print('\nNo Gender Data available for the selected city.')
        
    else:
        gender_count = df['Gender'].value_counts()
        print('\nGender Counts:\n', gender_count)
        

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print('No Year of Birth available for the selected city.')
        
    else:
        year_of_birth = df['Birth Year']
        print('\nEarliest Year of Birth: ',year_of_birth.min())
        print('Most Recent Year of Birth: ',year_of_birth.max())
        print('Most Common Year of Birth: ',year_of_birth.value_counts().index[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_display(city):
    """Displays 5 rows of Raw Data.""" 

    
    df = pd.read_csv(CITY_DATA[city])
    print('\nRaw data is available to check... \n')
    row_loc = 0
    while True:
        
        user_answer = input('\nWould you like to view 5 rows of individual trip data? Enter "Yes" or "No".\n').lower()
        if user_answer not in ('yes', 'no'):
            print('Invalid entry, please enter "Yes" or "No"')
        
        elif user_answer == 'yes':
            print(df.iloc[row_loc:row_loc + 5])
            row_loc += 5
        elif user_answer == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_display(city)

        restart = input('\nWould you like to restart? Enter "Yes" or "No".\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()