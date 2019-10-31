import sqlite3
import datetime
import pandas as pd
import matplotlib.pyplot as plt


# An own class for all this weird user interaction so the rest can be a lot of fun with data and databases
class UserInteraction:
    def __init__(self):
        self.input_warning = "Something might be wrong with your input, please check it."

    # Different options for the user
    def options(self):
        print("You have different options so choose what you want to do.")
        while True:
            user_input = input("Adding a new entry (1), checking the last entry (2), analyze it all (3) or leave (0)? ")
            try:
                user_input = int(user_input)

                if user_input == 0:
                    return 0
                elif user_input == 1:
                    print("Okay, you want to add a new entry.")
                    return 1
                elif user_input == 2:
                    print("Okay, you want to check the last entry.")
                    return 2
                elif user_input == 3:
                    print("Okay, have fun with data analyzing.")
                    return 3
                else:
                    print(self.input_warning)

            except ValueError:
                print(self.input_warning)

    @staticmethod
    def get_drink():
        user_input = input("What's your drink? ")

        return user_input

    def get_date(self):
        print("For data science and documentation, the date of your caffeine is important.")
        while True:
            # Option for today and other date
            user_input = input("Do you want to use the date of today (1) or another date (2)? ")

            try:
                user_input = int(user_input)
                if user_input == 1:
                    print("Okay, you want to use the date of today.")
                    today_date = datetime.date.today()
                    return today_date

                elif user_input == 2:
                    print("Okay, you want to check the last entry.")
                    date_options = ["year", "month", "day"]
                    date_input = []

                    # One for loop instead of three while loops because every potential mistake have to be checked
                    for option in date_options:
                        input_check = 0
                        while input_check == 0:
                            user_date = input(f"For which {option} do you want to input something? ")
                            try:
                                user_date = int(user_date)
                            except ValueError:
                                print(self.input_warning)

                            # Checking year, every number bigger 0 is okay
                            if option == "year":
                                if user_date > 0:
                                    date_input.append(user_date)
                                    input_check = 1

                            # Checking month, numbers between 1 and 12 are okay
                            elif option == "month":
                                if 0 < user_date < 13:
                                    date_input.append(user_date)
                                    input_check = 1

                            elif option == "day":
                                # some months have only 30 days
                                if date_input[1] in [4, 6, 9, 11]:
                                    if 0 < user_date < 31:
                                        date_input.append(user_date)
                                        input_check = 1

                                elif date_input[1] in [1, 3, 5, 7, 8, 10, 12]:
                                    if 0 < user_date < 32:
                                        date_input.append(user_date)
                                        input_check = 1

                                elif date_input[1] == 2:
                                    # some years are leap-years and so, february has 28 or 29 days (I hate dates)
                                    if (date_input[0] % 4 == 0) and (date_input[0] % 100 != 0) or (
                                            date_input[0] % 400 == 0):
                                        if 0 < user_date < 30:
                                            date_input.append(user_date)
                                            input_check = 1

                                    else:
                                        if 0 < user_date < 29:
                                            date_input.append(user_date)
                                            input_check = 1

                    # Pushing all the data of the user in one datetime
                    given_date = datetime.date(date_input[0], date_input[1], date_input[2])
                    return given_date

                else:
                    print(self.input_warning)

            except ValueError:
                print(self.input_warning)

    def get_caffeine(self):
        print("The concentration of caffeine in your drink is important and also the volume of your drink.")
        while True:
            user_input_conc = input("What is the concentration of caffeine in your drink? (mg/100 mL)? ")
            try:
                user_input_conc = int(user_input_conc)
                if 0 < user_input_conc < 1000:
                    while True:
                        user_input_vol = input("What is the volume of your drink? (mL) ")
                        try:
                            user_input_vol = int(user_input_vol)
                            if 0 < user_input_vol < 5000:
                                return user_input_conc, user_input_vol
                            else:
                                print(self.input_warning)

                        except ValueError:
                            print(self.input_warning)

                else:
                    print(self.input_warning)

            except ValueError:
                print(self.input_warning)


class CaffeineBase:
    def __init__(self):
        # Opens the database, if there isn't that file, it'll be created
        self.connection = sqlite3.connect("CaffeineBase.db")
        self.c = self.connection.cursor()
        # Creating the database if it's not existing with id, name of drink, date, amount of caffeine and drink
        self.c.execute('''CREATE TABLE IF NOT EXISTS nebula (id, drinkname, drinkdate, caffeine, drinkvolume);''')

    # Function for testing the whole input of database, function takes as arguments everything what's going to be put in
    def get_input(self, input_id, input_drinkname, input_drinkdate, input_caffeine, input_drinkvolume):
        # Executing the input into the database
        self.c.execute('''INSERT INTO nebula (id, drinkname, drinkdate, caffeine, drinkvolume)
        VALUES (?, ?, ?, ?, ?);''', (input_id, input_drinkname, input_drinkdate, input_caffeine, input_drinkvolume))
        # Commit for getting stuff in the table because without this, noting is written in the table
        self.connection.commit()

    # Function for seeing whole database content, actually, it was more for testing than for using but it shows
    # wonderful content for data analyzing
    def content(self):
        entry_list = []
        for row in self.c.execute('''SELECT * FROM nebula;'''):
            # Type of row    is tuple
            entry_list.append(row)

        return entry_list

    # Getting id, should be possible with SQLite too, but I found stuff like "avoid using autoincrement"
    def get_id(self):
        # Trying to begin with ID 0 and then counting for every entry one up
        try:
            last_entry = self.c.execute('''SELECT id FROM nebula ORDER BY id DESC LIMIT 1''')
            # It's only possible to call fetchone one time, I tried it with a print and it was always 0, without, old
            # value + 1, so I created a variable for the content of last_entry.fetchone()[0]
            last_entry_value = last_entry.fetchone()[0]
            new_entry_value = last_entry_value + 1

        # Type Error is raised if there is no value because nobody has gone there before. So start at the beginning
        # and the beginning is zero
        except TypeError:
            new_entry_value = 0

        return new_entry_value

    def get_last_input(self):
        last_entry = self.c.execute('''SELECT * FROM nebula ORDER BY id DESC LIMIT 1''')
        last_entry_value = last_entry.fetchone()

        # Can be empty if the database doesn't exist
        return last_entry_value


class DataAnalyzing:
    @staticmethod
    def get_dataframe(database_content_list):
        # Throwing away index which was in database
        tuple_changing = [cols[1:] for cols in database_content_list]
        # Getting the list backwards so the last date is the last entry
        backwards = list(reversed(tuple_changing))
        # Creating the actual DataFrame with columns
        framed_entries = pd.DataFrame(backwards, columns=["drink", "date", "concentration (mg/100mL)", "volume (mL)"])

        return framed_entries

    # Getting the frequency of every drink for every entry in the database and dataframe
    @staticmethod
    def get_drink_frequency(drink_frame):
        drink_frame = drink_frame["drink"].value_counts()

        return drink_frame

    # Function for plotting the frequency of every drink
    @staticmethod
    def frequency_plotting(frequency_frame):
        plt.figure()
        my_colors = [(1.0, 0.776, 0), (0, 0.463, 0.729), (0.6, 0.729, 0), (0, 0.463, 0.729)]
        frequency_frame.plot.pie(colors = [(1.0, 0.776, 0), (0.6, 0.729, 0), (0, 0.463, 0.729), (0.6, 0.729, 0)])
        plt.ylabel('')
        plt.show()

    # Two line function for creating a new column in a dataframe which isn't that complicated (surprise)
    @staticmethod
    def get_mass_dataframe(existing_frame):
        # Getting the values of concentration and volume in a series so it's possible to calculate the mass of caffeine
        existing_frame["mass (mg)"] = (existing_frame["concentration (mg/100mL)"] / 100) * existing_frame["volume (mL)"]

        return existing_frame

    @staticmethod
    def bar_mass_plotting(mass_frame):
        # Throwing away all the data but mass of caffeine
        edit_mass_frame = mass_frame.drop(columns=["concentration (mg/100mL)", "volume (mL)"], axis=1)
        edit_mass_frame = edit_mass_frame.groupby("date")["mass (mg)"].sum()
        plt.figure()
        # Plotting data in normal plot and bar plot
        edit_mass_frame.plot(x="date", color = (1.0,0.776,0))
        plt.show()
        edit_mass_frame.plot.hist(orientation='horizontal', cumulative=True)
        plt.show()

        return edit_mass_frame

    @staticmethod
    def total_sums(full_frame):
        total_mass = full_frame["mass (mg)"].sum()
        total_volume = full_frame["volume (mL)"].sum()

        return total_mass, total_volume


def main():
    coffee = CaffeineBase()
    talk = UserInteraction()
    bamboo = DataAnalyzing()

    print("Welcome to a caffeine counter for saving your consume of caffeine. Yay.")
    while True:
        user_decision = talk.options()
        if user_decision == 1:
            input_id = coffee.get_id()
            input_drink = talk.get_drink()
            input_date = talk.get_date()
            input_caffeine = talk.get_caffeine()
            coffee.get_input(input_id, input_drink, input_date, input_caffeine[0], input_caffeine[1])

        elif user_decision == 2:
            print(f"The last entry was: {coffee.get_last_input()}")

        elif user_decision == 3:
            content_list = coffee.content()
            framed_content = bamboo.get_dataframe(content_list)
            drink_frame = bamboo.get_drink_frequency(framed_content)
            bamboo.frequency_plotting(drink_frame)
            ready_frame = bamboo.get_mass_dataframe(framed_content)
            bamboo.bar_mass_plotting(ready_frame)
            all_mass, all_volume = bamboo.total_sums(ready_frame)
            print(f"The total mass of caffeine is {all_mass} mg and the total volume is {all_volume} mL.")

        else:
            break

    print("Goodbye!")


main()
