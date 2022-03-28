import sqlite3
import csv

# initialize the database
def create_db():
    try:
        # create db
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # create finals_mvp table
        c.execute('''CREATE TABLE IF NOT EXISTS finals_mvp
                    (
                    fld_year INTEGER,
                    fld_finals_mvp TEXT,
                    fld_age INTEGER,
                    fld_team TEXT,
                    fld_pts FLOAT,
                    fld_trb FLOAT,
                    fld_ast FLOAT
                    );''')

        # opens csv and inserts into db, doesn't insert twice
        num_row = int(c.execute("SELECT COUNT(*) FROM finals_mvp").fetchall()[0][0])
        if num_row == 0:
            with open('finals_mvp.csv', 'r') as fin:
                dr = csv.DictReader(fin)
                finals_mvp_data = [(i['Year'], i['Finals MVP'], i['Age'], i['Team'], i['PTS'], i['TRB'], i['AST']) for i in dr]

            insert_records = "INSERT INTO finals_mvp (fld_year, fld_finals_mvp, fld_age, fld_team, fld_pts, fld_trb, fld_ast) VALUES(?, ?, ?, ?, ?, ?, ?);"
            c.executemany(insert_records, finals_mvp_data)

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # create nba_champions table
        c.execute('''CREATE TABLE IF NOT EXISTS nba_champions
                    (
                    fld_year INTEGER,
                    fld_champion TEXT,
                    fld_runner_up TEXT,
                    fld_finals_mvp TEXT,
                    fld_points TEXT,
                    fld_rebounds TEXT,
                    fld_assists TEXT
                    );''')

        # opens csv and inserts into db, doesn't insert twice
        num_row = int(c.execute("SELECT COUNT(*) FROM nba_champions").fetchall()[0][0])
        if num_row == 0:
            with open('nba_champions.csv', 'r') as fin:
                dr = csv.DictReader(fin)
                nba_champions_data = [(i['Year'], i['Champion'], i['Runner-Up'], i['Finals MVP'], i['Points'], i['Rebounds'], i['Assists']) for i in dr]

            insert_records = "INSERT INTO nba_champions (fld_year, fld_champion, fld_runner_up, fld_finals_mvp, fld_points, fld_rebounds, fld_assists) VALUES(?, ?, ?, ?, ?, ?, ?);"
            c.executemany(insert_records, nba_champions_data)

        # finish closing db
        conn.commit()

        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


# prints instructions
def show_instructions():

    print("\n<*-------------------------------------------------------------------------------------*>")

    print("Welcome to the instructions!")

    print("The following is a guide to structuring your queries.\n")

    print("The first value to input is the year.\n")

    print("The second value is more complicated.\n")

    print("If you would like to find the winner, runner up or finals MVP, simply finish your query")

    print("with the keyword 'Champions', 'Runner Up' or 'MVP'.\n")

    print("If you would like to search for a certain stat, that should be the third phrase in your query.\n")

    print("Here is an example: 2014 Champions\n")

    print("Here is another: 1999 MVP Points\n")

    print("Lastly, if any keyword is two words, such as Runner Up, it needs to be surrounded by double")

    print("quotation marks. \n")

    print("Enter 'help' for more instructions.")


# display the help instruction and prompt an input to show the details
def help_user():
    try:
        keep_going = True
        # Allow user to pick between 4 choices
        while keep_going:
            print("\nSelect from the help menu below")
            print("1. Show instructions")
            print("2. Show available stats options")
            print("3. Data summary")
            print("4. Exit")

            # Calls show_instructions function again
            user_choice = int(input("Choose option: "))
            if user_choice == 1:
                show_instructions()

            # Display the three available stats
            elif user_choice == 2:
                print("\nThe available stats to search for include: Points, Assists, and Rebounds.")
                print("You may also search for an MVP's age.\n")
                print("You may also enter query the number of rows by entering 'total rows'.")

            # Display summary of the data
            elif user_choice == 3:
                print("\nWe are using data on the NBA Finals and NBA MVPs.\nThe NBA Finals table has columns for Year, Finals MVP, Age, Team, Points, Rebounds, and Assists. \n"
                      "The Finals MVP table has columns for Year, Champion, Runner-Up, Finals MVP, Points, Rebounds, Assists. \n")

            # Exit the help menu
            elif user_choice == 4:
                keep_going = False

            else:
                print("Please choose one of the valid options.")
    except ValueError:
        error()


# Determine which query should be executed according to the incoming command array modified by the parse function
def query_db(user_input):
    # open db and set variables
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    string_year = str(user_input[0])
    try:
        # get total rows
        if user_input[0] == "total":
            if len(user_input) == 2:
                if user_input[1] == "rows":
                    final_query = "SELECT COUNT(*) AS rows FROM finals_mvp"
                    rows = c.execute(final_query).fetchall()
                    print(rows[0][0])
                else:
                    error()
            else:
                error()

        # all regular queries
        elif 1980 <= int(user_input[0]) <= 2021:
            if len(user_input) == 2:
                # gets nba champion by year
                if user_input[1] == "champions":
                    query = "SELECT fld_champion FROM nba_champions WHERE fld_year = "
                    final_query = query + string_year
                    rows = c.execute(final_query).fetchall()
                    print(rows[0][0])

                # gets runner up by year
                elif user_input[1] == "runner-up" or user_input[1] == "runner up":
                    query = "SELECT fld_runner_up FROM nba_champions WHERE fld_year = "
                    final_query = query + string_year
                    rows = c.execute(final_query).fetchall()
                    print(rows[0][0])

                # gets mvp by year
                elif user_input[1] == "mvp":
                    query = "SELECT fld_finals_mvp FROM finals_mvp WHERE fld_year = "
                    final_query = query + string_year
                    rows = c.execute(final_query).fetchall()
                    print(rows[0][0])

                else:
                    error()

            elif len(user_input) == 3:
                # select points, rebounds, or assists from the finals
                if user_input[1] == "finals":
                    field = ""
                    if user_input[2] == "points":
                        field = "fld_points"
                        final_query = "SELECT " + field + " FROM nba_champions WHERE fld_year = " + string_year
                        rows = c.execute(final_query).fetchall()
                        print(rows[0][0])

                    elif user_input[2] == "assists":
                        field = "fld_assists"
                        final_query = "SELECT " + field + " FROM nba_champions WHERE fld_year = " + string_year
                        rows = c.execute(final_query).fetchall()
                        print(rows[0][0])

                    elif user_input[2] == "rebounds":
                        field = "fld_rebounds"
                        final_query = "SELECT " + field + " FROM nba_champions WHERE fld_year = " + string_year
                        rows = c.execute(final_query).fetchall()
                        print(rows[0][0])

                    else:
                        error()

                # gets points, rebounds, or assists from mvp
                elif user_input[1] == "mvp":
                    field = ""
                    if user_input[2] == "points":
                        field = "fld_pts"
                        final_query = "SELECT " + field + " FROM finals_mvp WHERE fld_year = " + string_year
                        rows = c.execute(final_query).fetchall()
                        print(rows[0][0])

                    elif user_input[2] == "assists":
                        field = "fld_ast"
                        final_query = "SELECT " + field + " FROM finals_mvp WHERE fld_year = " + string_year
                        rows = c.execute(final_query).fetchall()
                        print(rows[0][0])

                    elif user_input[2] == "rebounds":
                        field = "fld_trb"
                        final_query = "SELECT " + field + " FROM finals_mvp WHERE fld_year = " + string_year
                        rows = c.execute(final_query).fetchall()
                        print(rows[0][0])

                    # gets age of mvp by the year, JOIN statement HERE!!!!!!!!!!
                    elif user_input[2] == "age":
                        final_query = "SELECT finals_mvp.fld_age FROM nba_champions INNER JOIN finals_mvp ON nba_champions.fld_finals_mvp=finals_mvp.fld_finals_mvp WHERE finals_mvp.fld_year = "+ string_year
                        rows = c.execute(final_query).fetchall()
                        print(rows[0][0])

                    else:
                        error()

                else:
                    error()

            else:
                error()

        else:
            error()

    except ValueError:
        error()


# prints error message
def error():
    print('Invalid Input')
    print('Enter "help" for help menu')


# prompt an input as the sql command
def prompt_command():
    command = (input(str("\nEnter your query:\n>")))
    while (command == "") | (command == " "):
        error()
        command = (input(str("\nEnter your query:\n>")))
    command = command.replace("\'", "\"") # replace all the single quotation marks to double quotation marks
    return command.lower()


# parse the command
def parse_the_command(command):
    phrase = [] # initialize the array which would be returned
    if "\"" in command:
        if (command.count("\"") % 2) != 0: # check if the # of '"' is even
            error()
            return []
        else:
            while "\"" in command:              # put the content between a pair of quotation marks as a whole element
                squo_index = command.find("\"")
                equo_index = command.find("\"", squo_index+1)
                before = command[:squo_index]
                before_split = before.split(" ")
                phrase += before_split
                phrase.append(command[squo_index+1:equo_index])
                command = command[equo_index+1:]

    phrase += command.split(" ")
    while "" in phrase:     # remove all empty elements
        phrase.remove("")

    return phrase

# main function
if __name__ == "__main__":
    # call func to create db
    create_db()

    # initialize string variable command to empty string
    command = ""

    # display instructions to user
    show_instructions()

    # while loop to allow user to continue querying until they enter 'exit'
    while command != "exit":

        # call prompt command and store result in command string variable from line 291
        command = prompt_command()

        # call parse_the_command on the command variable to parse through the user's query
        user_input = parse_the_command(command)

        # if command is not exit
        if command != "exit":

            # if command is help, enter help menu
            if user_input[0] == "Help" or user_input[0] == "help":
                help_user()

            # else query the db with users query
            else:
                query_db(user_input)
