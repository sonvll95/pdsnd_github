import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Define lists of valid cities, months, and days
    valid_cities = ["chicago", "new york city", "washington"]
    # Valid months for analysis (all lowercase)
    valid_months = [month.lower() for month in calendar.month_name[1:]] + ["all"]

    # Valid days of the week for analysis (all lowercase)
    valid_days = [day.lower() for day in calendar.day_name] + ["all"]
    
    # Prompt user for city until a valid city is entered
    while True:
        city = input("Enter city (chicago, new york city, washington): ").lower()
        if city in valid_cities:
            break
        else:
            print("You have entered an incorrect city. Please try again.")
    
    # Prompt user for month until a valid month is entered
    while True:
        month = input("Enter month: (all, january, february, ..., june): ").lower()
        if month in valid_months:
            break
        else:
            print("You have entered an incorrect month. Please try again.")
    
    # Prompt user for day until a valid day is entered
    while True:
        day = input("Enter day of week: (all, monday, tuesday, ..., sunday): ").lower()
        if day in valid_days:
            break
        else:
            print("You have entered an incorrect day. Please try again.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()  

    if month != 'all':
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("The most common month is:", df['month'].mode()[0])

    print("The most common month is:", df['day_of_week'].mode()[0])

    df['start_hour'] = df['Start Time'].dt.hour
    print("The most common start hour is:", df['start_hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("The most commonly used start station:", df['Start Station'].value_counts().idxmax())

    print("The most commonly used end station:", df['End Station'].value_counts().idxmax())

    df['Station Combination'] = df['Start Station'] + ' to ' + df['End Station']

    # Find the most frequent combination
    most_frequent_combination = df['Station Combination'].value_counts().idxmax()

    print("The most frequent combination of start station and end station trip:", most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    total_travel_time = (df['End Time'] - df['Start Time']).sum()
    print("Total travel time:", total_travel_time)

    mean_travel_time = (df['End Time'] - df['Start Time']).mean()
    print("Mean travel time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("Counts of user types:", df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print("Counts of gender:")
        print(df['Gender'].value_counts())
    else: 
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # Display earliest, most recent, and most common year of birth (if available)
    if 'Birth Year' in df.columns:
        print("Earliest year of birth:", df['Birth Year'].min())
        print("Most recent year of birth:", df['Birth Year'].max())
        print("Most common year of birth:", df['Birth Year'].mode()[0])
    else:
        print("Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe")

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

        raw_data_display = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if raw_data_display.lower() == 'yes':
            row_index = 0
            while True:
                print(df.iloc[row_index:row_index + 5])
                row_index += 5
                raw_data_display = input('\nWould you like to see more raw data? Enter yes or no.\n')
                if raw_data_display.lower() != 'yes' or row_index >= len(df):
                    break  
        elif raw_data_display.lower() != 'yes':
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
