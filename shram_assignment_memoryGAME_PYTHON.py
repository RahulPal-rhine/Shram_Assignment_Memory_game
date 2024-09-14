#MemoryGame
import mysql
import mysql.connector
conn = mysql.connector.connect(host = 'localhost', password = 'sql123', username = 'rahul', database = 'Memory_Game' )
import random

#to work with database we call cursor() and store it in a variable
mycursor = conn.cursor(buffered= True)

#Rules of Memory game
rules = """
******************** Rules/Flow of the game *************************************
1. if playing for 1st time here then player to enter username to store in database.
2. Player will see a list of 12 cards with no face just a black string
    eg  [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
3. The player turns over 2 cards by entering number from 1 to 12 
   Number 1 represents the first card out of 12 cards and so on....
4. If 1st and 2nd guesses matches the value of both cards then bingo player is just need to guess remaining cards.
   If not then all will become as blank state and player need to start making guesses. 
5. This goes on untill all the matching pair cards have been correctly guess.
6. After finishing the game, PLayer can choose to continue or stop the game.
"""

print(rules)
# imagine numbers as a position of the cards.
board_numbers = [
'1','2','3',
'4','5','6',
'7','8','9',
'10','11','12'
]
print("Below is the list that contains 12 cards represented in numbers 1 to 12.")
print(board_numbers)

# different cards with a single pair 
signs = [
'@','#','@',
'%','&','*',
'#','$','$',
'&','*','%'
]
#print(signs)
highest_score = 0
new_game_high_score = highest_score
score = 0
past_scores = []


moves = []
total_moves = 0
multi_game_scores = []
#print(random_signs)
new_game = False
while not new_game:

    user_name = input("\nEnter username: ")
        # Check if the username already exists in the database
    mycursor.execute("SELECT * FROM Login WHERE user_name = %s", (user_name,))
    result = mycursor.fetchall()

    if result:
            print("Username already exists in the database!")
            print("Below are your past scores and highest score from the last game.")
            mycursor.execute("SELECT highest_score,score FROM Login WHERE user_name = %s", (user_name,))
            user_data = mycursor.fetchone()

            # Display the user's records
            print("Username:", user_name)
            print("Past Highest Score:", user_data[0])
            print("Past score:", user_data[1])



    else:
            fresh_username = "INSERT INTO Login (user_name, highest_score, score) VALUES (%s,%s,%s)"
            value = (user_name,highest_score,score)
            mycursor.execute(fresh_username,value)
            conn.commit()
            print(f"Username : '{user_name}' inserted successfully in database!")

    #making the elements position random every time user plays new game  
    random_signs = random.sample(signs,len(signs))
    #print(random_signs)

    #to store the user's guesses (acting as backstage)
    backend_board = [
        ' ',' ',' ',
        ' ',' ',' ',
        ' ',' ',' ',
        ' ',' ',' '
    ]
    print("\n" *2)
    print("Below is the cards shown as blank. Please make a guess by entering a number to see the value of a card.")
    print(backend_board)


    #to store and check the counts of the moves, specially only 2 moves.
    flap_check = []

    #to store the guess and display only the matched pair
    result_board = [
        ' ',' ',' ',
        ' ',' ',' ',
        ' ',' ',' ',
        ' ',' ',' '
    ]
#creating username to store it in database table
        



    #continously taking input from user until the game is over
    game_over = False
    while not game_over:
        


        #taking user input in string and storing it in string.
        user_input = input("\nEnter a number: ")

        #created an empty value strings to use to display the list as empty.
        frontend_board = [
        ' ',' ',' ',
        ' ',' ',' ',
        ' ',' ',' ',
        ' ',' ',' '
    ]

        for row in board_numbers:
                
            if user_input == row:
                user_input = int(user_input) - 1 #index
                backend_board[user_input] = random_signs[user_input] ######
                value = backend_board[user_input]
                flap_check.append(value)
                
                if len(flap_check) == 2:
                    moves.append(1)
                    flap_check = []
                    if backend_board.count(value) == 2:
                        result_board = backend_board.copy()
                        print('It is match!')
                        print(result_board)
                        
                    else:
                        print('Tts a miss !' )
                        print(backend_board)
                        backend_board = frontend_board.copy()
                        backend_board = result_board.copy()
            
                else:
                    print(backend_board)
                    break
                break
            else:
                game_over = False
        if ' ' in result_board:
            continue
        else:
            game_over = True
            print("***************** You Won ***********************")

            #for calculating total_moves from a list
            for score in moves:
                total_moves += moves[score]

            
            past_scores.append(total_moves)
            #inserting past_scores in database
            for score in past_scores:
                score_update = ("UPDATE Login set score = %s WHERE user_name = %s")
                score_value = (score,user_name)
                mycursor.execute(score_update,score_value)
                
            # past_moves = "INSERT INTO Login (past_scores) VALUES (%s)"
            # value = (past_scores,)
            # mycursor.execute(past_moves,value)

            print(f"Your total moves was {total_moves}")
            highest_score = min(past_scores)
            print(f"Your highest score is : {highest_score}")

            #inserting highest_score in database
            high_move = ("UPDATE Login set highest_score = %s WHERE user_name = %s")
            value = (highest_score,user_name)
            mycursor.execute(high_move,value)
            conn.commit()


            



            new_game  = input("Do you want to continue with next game? \nType 'y' for yes and 'n' for No: ").lower()
            

# fresh_username = "INSERT INTO Login (user_name, highest_score, score) VALUES (%s,%s,%s)"
#             value = (user_name,highest_score,score)
#             mycursor.execute(fresh_username,value)

    if new_game == 'y':
        # new_game_high_score = highest_score
        # new_game = False 
        highest_score = 0
        score = 0
        insert_new_row = "INSERT INTO Login (user_name, highest_score, score) VALUES (%s,%s,%s)"
        values= (user_name,highest_score,score)
        mycursor.execute(insert_new_row,values)
        conn.commit()
        new_game = False
        continue

    elif new_game == 'n':
            all_players_record = input("Type 'y' to see 10 players records.")
            if all_players_record == 'y':
                 mycursor.execute("SELECT * FROM Login")
                 for data in mycursor.fetchall():
                    print(data)
            new_game = True
            break
    else:
            print("Enter valid input")
            break
        
        



