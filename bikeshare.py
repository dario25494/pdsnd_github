import time
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
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for month (all, january, february, ... , june)
    while True:
        city = input('Enter the name of the city of your interest among chicago, new york city and washington:\n').lower().strip()
        if city not in ['chicago','new york city','washington']:
            print('\nname not valid\n')
        else:
            break
    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the name of the month of your interest from january to june (digit 'all' for data relating to all months):\n").lower().strip()
        if month not in ['all','january','february','march','april','may','june']:
            print('\nname not valid\n')
        else:
            break
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter the name of the day of the week of your interest (digit 'all' for data relating to all days):\n").lower().strip()
        if day not in ['all','monday','thursday','wednesday','thursday','friday','saturday','sunday']:
            print('\nname not valid\n')
        else:
            break

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    answer=input('do you want to see raw data in batches of five rows? type yes if you want').lower().strip()
    i=0
    while answer=='yes':
        print(df[i:i+5])
        answer=input('type yes to see other 5 rows of data').lower().strip()
        i+=5
        if i> len(df):
            break
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Display the most common month
    most_common_month = df['Start Time'].dt.month.mode()[0]
    count_month= df['Start Time'].dt.month.value_counts()[most_common_month]
    print('the most common month is {} with a number of times of {}'.format(most_common_month, count_month))

    # Display the most common day of week
    most_common_day = df['Start Time'].dt.day.mode()[0]
    count_day= df['Start Time'].dt.day.value_counts()[most_common_day]
    print('the most common day is {} with a number of times of {}'.format(most_common_day, count_day))

    # Display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    count_hour=df['Start Time'].dt.hour.value_counts()[most_common_start_hour]
    print('the most common start hour is {} with a number of times of {}'.format(most_common_start_hour, count_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    max_1=df['Start Station'].value_counts().max()
    most_commonly_used_start_station = df['Start Station'].value_counts()[df['Start Station'].value_counts()==max_1].index[0]
    print('the most common used Start Station is {} with a number of times of {}'.format(most_commonly_used_start_station, max_1))



    # Display most commonly used end station
    max_2=df['End Station'].value_counts().max()
    most_commonly_used_end_station = df['End Station'].value_counts()[df['End Station'].value_counts()==max_2].index[0]
    print('the most common used End Station is {} with a number of times of {}'.format(most_commonly_used_end_station, max_2))


    # Display most frequent combination of start station and end station trip
    df['combination']=df['Start Station']+ '-' +df['End Station']
    max_3=df['combination'].value_counts().max()
    most_frequent_combination = df['combination'].value_counts()[df['combination'].value_counts()==max_3].index[0]
    print('the most frequent combination is {} with a number of times of {}'.format(most_frequent_combination, max_3))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('the total travel time is: {}'.format(total_travel_time))
    # Display mean travel time
    average_travel_time = df['Trip Duration'].mean(axis=0)
    print('the average travel time is: {}'.format(average_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print( 'The number of users per each type is \n{}'.format(df.groupby(['User Type'])['Unnamed: 0'].count()))

    # Display counts of gender
    try:
        print( 'The number of users per gender is \n{}'.format(df.groupby(['Gender'])['Unnamed: 0'].count()))
    except:
        print('For the city of Washington there aren\' t informations regarding the users gender')


    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = df['Birth Year'].min()
        print('The earliest year of birth is {}'.format(earliest_year_of_birth))

        most_recent_year_of_birth = df['Birth Year'].max()
        print('The most recent year of birth is {}'.format(most_recent_year_of_birth))

        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print('The most common year of birth is {}'.format(most_common_year_of_birth))
    except:
        print('For the city of Washington there aren\' t informations regarding the users birth year')

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
