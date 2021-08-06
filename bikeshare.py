import time
import pandas as pd
import numpy as np

#Creating dictionary for city, and the filename
CITY_DATA = { 'chicago': 'chicago.csv',
              'washington': 'washington.csv',
              'new york city': 'new_york_city.csv' }

#Creating tuple for Month_Name
MONTH_NAME = ['jan','feb','mar','apr','may','jun']

#Creating tuple for day of the week
DAY_OF_WEEK = ['mon','tue','wed','thu','fri','sat','sun']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("Please enter the city name from valid list: Chicago, New York City, Washington ").lower()
        if city in CITY_DATA:
            break
        else:
            print("You entered incorrect City Name")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please choose any month from Jan to Jun to filter by, or 'all' to apply no day filter.").lower()[:3]
        if month in MONTH_NAME or month == 'all':
           break
        else:
           print("You entered incorrect value for Month")

# get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter name of the day of week to filter by, or 'all' to apply no day filter: ").lower()[:3]
        if day in DAY_OF_WEEK or day == 'all':
            break
        else:
            print("You entered incorrect value for Day of Week")

    print('-'*40)
    print("You choose to see the Bike share data statistics of {} city for {} month(s) and {} as day of week(s)".format(city, month, day))
    #Return the filter information
    return city,month,day


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
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    if month != 'all':
        # Converting month name to digit METHOD 1
        month = MONTH_NAME.index(month) + 1
        #METHOD 2
        # month = (dt.datetime.strptime(month, '%b')).month
        # Filtering data based on month
        df = df[df['month'] == month]

    if day != 'all':
        #Converting Day of week to digit
        day = DAY_OF_WEEK.index(day) + 1
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most Common Month is: ",df['month'].mode()[0])

    # display the most common day of week
    print("Most Common Day of week is: ", df['day_of_week'].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("Most Common Hour is: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_point = df['Start Station'].mode()[0]
    print("Most Common Start Station is: ",most_common_start_point)

    # display most commonly used end station
    most_common_end_point = df['End Station'].mode()[0]
    print("Most Common End Station is: ",most_common_end_point)

    # display most frequent combination of start station and end station trip
    most_common_start_end_point = df[['Start Station','End Station']].mode().loc[0]
    print("Most Common Start and End Station are {}, and {} respectively: ".format(most_common_start_end_point[0],most_common_start_end_point[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round((df['Trip Duration'].sum() / 360), 2)
    print("Total travel time is: {} hours".format(total_travel_time))

    # display mean travel time
    average_travel_time = round((df['Trip Duration'].mean() / 360), 2)
    print("Average travel time is: {} hours".format(average_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("Count of records based on User Type :"'\n', user_type_count)

    if 'Gender' in df or 'Birth Year' in df:
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print("Count of records based on Gender :"'\n', gender_count)

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print("Earliest Birth Year is {}\nMost Recent Birth Year is {}\nMost common birth year is {}: ".format(earliest_birth_year, recent_birth_year, common_birth_year))

    else:
        print('Gender and Birth Year are not available for your selected city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays the raw data."""
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        if view_data in ('yes', 'no'):
            break
        else:
            print("You entered incorrect value for Month. Please try again.")

    index = 0
    while view_data == 'yes':
        print(df.iloc[index:index + 5])
        index += 5
        view_data = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()