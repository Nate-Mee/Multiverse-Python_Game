from datetime import datetime as dt 
from datetime import timedelta as td
from google.colab import output
import random

#set up global variables
case_file = {}
locations = {}
sec_room_completed_dict = {"Open Emails":0, "Open Desk Drawer":0, "Open CCTV History":0}
b_counter = 0
m_counter = 0
c_counter = 0
riddle = """I'm a constant in life yet you rarely think of me.
I'm smaller than four yet bigger than three.
I go on forever yet never repeat.
Just add an 'e' and I'm ready to eat!
"""
password_hints = [
    "Hanks kid did seem pretty into the colour red, maybe that has something to do with it.\n", 
    "Maybe I should check my case file for clues.\n", 
    "That post-it with 'ColourNumberSymbol' seemed pretty important.\n", 
    "You hit the keyboard...shockingly that did not help.\n"
    "If I were Hank, what would my password be...\n"
    ]

#takes up to 9 strings or a list of strings, numbers them in the order provided, 
#asks the user to choose one and prints/returns that choice. 
#(Could take more than 9 if ok returning with number at start - remove [3:] in return statement)
def give_options(*options):
    #define variables
    opt_dict = {}
    counter = 1   
    #create dictionary of options(arguments)
    for option in options:
        if type(option) == list:
            for num in range(0, len(option)):
                opt_dict[counter] = str(counter) + ". " + option[num]
                counter += 1
        else:
            option = str(option)
            opt_dict[counter] = str(counter) + ". " + option
            counter += 1
    #print options
    print("These are your options:")
    for num in range(1, counter):
        print(opt_dict[num])
    #take user choice and print it
    while True:
        try:
            choice = opt_dict[int(input("Please enter a number to make your choice: "))]
            output.clear()
            print(f"You chose: {choice}")
            return choice[3:]
        except:
            print("Invalid input, please try again.")
            continue
        break

#to print casefile - may not be needed in final code, here to test
#could be used to print out key/value pairs in any dict
def print_dict(dict):
    for key in dict:
        print(f"{key} - {dict[key]}\n")


#takes an integer for the number of guesses to allow
def incorrect_entry_counter(num_of_attempts):
    print(f"That was incorrect. You have {num_of_attempts - 1} trys remaining.\n")
    return num_of_attempts - 1

def split_string_to_list(string):
    lst = []
    for char in string:
        lst.append(char)
    return lst

#takes the number of attempts you want to allow (int), lockout time in whole minutes (int) if limit reached 
#a clue that is a string (Could just be "\n") and any number of single digits (str) that make up the passcode,
#returns True if user correct and current time if they ran out of guesses (as datetime type)
def numerical_passcode(attempts_allowed, lockout_duration, clue, *numbers):
    #define variables
    numbers = list(numbers)
    passcode_length = len(numbers)
    now = dt.now()
    try:
        complete_passcode = "".join(numbers)
    except: 
        print("Those passcode numbers weren't strings were they...")
    num_dict = {}
    #take and test user input
    while True:
        try:
            user_input = input("Please enter the passcode: ")
            #test if user was correct
            if user_input == complete_passcode:
                return True
            int(user_input)
        except:
            print("Please enter only numbers.")
            continue
        if len(user_input) != passcode_length:
            print(f"Please enter {passcode_length} numbers.")
            continue
        output.clear()
        #tell user how many attempts they have left
        attempts_allowed = incorrect_entry_counter(attempts_allowed)
        if attempts_allowed < 1:
            print(f"You are out of attempts and have been locked out for {lockout_duration} minutes.")
            return [now, lockout_duration]
        #reprint clue
        print(clue)
        #tell user which numbers were correct
        user_input_list = split_string_to_list(user_input)
        corr_num = ""
        for num in range(0, passcode_length):
            if user_input_list[num] == numbers[num]:
                corr_num = corr_num + " " + user_input_list[num]
            else:
                corr_num += " _"
        print(f"Any numbers you got correct are shown below:\n {corr_num}\n")

#takes a list with a time the lockout was triggered and the length of the lockout (output of numerical_passcode function)
#checks whether the time has expired or not and returns True or a string containing the time left locked out
def check_lockout_time(input_list):
    trigger_time = input_list[0]
    lockout_duration = input_list[1]
    now = dt.now()
    lockout_end = trigger_time + td(minutes=lockout_duration)
    time_left = str(lockout_end - now)
    if lockout_end <= now:
        return True
    else:
        return time_left.split('.')[0]

#takes a correct password string and checks if it matches the user input password.
#password is not case sensitive
#asks after every incorrect guess if they want to try again. Returns True or False
def password_check(password):
    password_l = password.lower()
    while True:
        user_input = input("Please enter the password: \n").lower()
        output.clear()
        #they get it right
        if user_input == password_l:
            print(f"{password} was correct.")
            case_file["Security CCTV Password"] = password_l
            return True
        #they get it wrong
        else:
            print("Incorrect Password.")
            print(random.choice(password_hints))
            while True:
                for char in user_input:
                    if char == " " or char == "_":
                        print("Passwords must not include spaces or underscores.")
                        break
                while True:
                    try_again = input("Would you like to try again? (y/n)\n")
                    output.clear()
                    if try_again != "y" and try_again != "n":
                        print("Please enter y or n.\n")
                    else:
                        break
                if try_again == "y":
                    break
                elif try_again == "n":
                    return False


#takes no arguments. Allows the user to view the three email options to get clues for CCTV password.
#one from mum, one from child, one from boss.
#adds more explicit tips to case file if don't get it at the time.
#Returns the number of emails that were viewed
def open_emails():
    print("""This mailbox is a mess, it doesn't look like a single message has ever been deleted.
There are clearly three main people sending Hank the Security Operative emails;
His Boss. His Mother. And a Child (presumably...hopefully, his Child).\n""")
    #counters mean emails only marked as completed and removed as an option if all have been read
    global b_counter, m_counter, c_counter
    while True:
        email_choice = give_options("Boss Email", "Mum Email", "Child Email", "Close Email")
        if email_choice == "Boss Email":
            print("""<Ignatius.Smith@bigbossman.org>
<Subject: Persistent Post-it Problem>
<Hello Hank,
 We have spoken about this numerous times but it was particularly embarrassing yesterday when
 I was showing Deborah (the new director) around. 
 I can't believe I have to spell this out again but Security need to be following
 company security practices. It feels like that should be obvious.
 I will be visiting on Tuesday and if I see one solitary post-it I will see to it 
 that you are post-ed to janitorial.
 Yours reluctantly,
 Ignatius Smith
 Head of Building Services>\n""")
            case_file[email_choice] = """Hanks post-it addiction is making him less of a security guard 
and more of a security risk. Also, his boss is an ass."""
            b_counter = 1
            print("The post-it with 'Ignoramus Smith - Tuesday' now makes a lot more sense.\n")
        elif email_choice == "Mum Email":
            print("""<mumsymum1865@mail.com>
<Subject: HHGTTG>
<Hello Darling!!! Do you know where my copy of Hitchikers is? I seem to have misplaced it!!!!!
 What with you turning 42 soon I thought I might read it again, what an amazing book!!!!!!!!
 Also I just saw Thomas (Tony the plumbers' son, Tony Perkins, the good plumber, not Tony Parker
 the bad plumber!! You know, the one that did Anita's kitchen where the taps fell off!!!).
 Anyway Thomas just went into Darleen's house and was there for almost 4 hours!!!! That's a lot 
 of time to lay a little pipe!!! Darleen did say at Friday's WI meeting that she had a leaky faucet 
 but I don't know, seems suspicious to me!!!!! I will mention it to the vicar on Sunday just in case!!
 Lots of love my little honey dumpling!! Mumsy xxxxxxxxxx>\n""")
            case_file[email_choice] = """Hank's mum's love of frivolous gossip is 
outweighed only by her love of exclamation marks. Hank turns 42 soon."""
            m_counter = 1
            print("You take a minute to let the nausea subside before continuing.\n")
        elif email_choice == "Child Email":
            print("""<racecarnuber1fasterestevr@thetrak.com>
<Subject: caaaaaaarz>
<Hallo dad my name is Alex and i like cars do you like cars my favrit car is red
 red is the best all the best cars are red do you like red lots and lots and lots of love hony dumps Alex>\n""")
            case_file[email_choice] = "The kid likes Red. Does not like punctuation."
            c_counter = 1
            print("How...special...\n")
        else:
          break
    print("You close Email and record what little you learned in your case file.\n")
    return b_counter + m_counter + c_counter

#Security Room, takes no arguments, complete room function, returns give_options string for room to go to.
def security_room():
    print("""The room is small and dark with just enough room for a desk, chair and computer
below a wall of monitors displaying live feeds across the site.
You step across the room in one large stride and take a seat at the desk.
You grab a post-it and scribble the door code on it, don't want to forget that.
Glancing at the monitors you notice Sarah looking shifty by the bins and David
'borrowing' Lucy's milk in the kitchenette. There is one dark screen on the desk in front of you,
surrounded by a rainbow of post-it notes. The desk is also covered in post-its,
some that appear to have been stuck there intentionally and others that have clearly
been left to rest where they have curled and dried with age eventually becoming
unstuck from the screen to drift into the gaudy sea below. Most are illegible or nonsensical,
there is one in particular that stands out though, written in thick sharpie in
pride of place at the centre of the top edge of the monitor. It reads: 'ColourNumberSymbol'.
You wiggle the mouse and the screen comes to life (the part not obstructed by post-its anyway).\n""")
    case_file["Security Room"] = """Hank needs to get his ducks in a row, security is a shambles
That post-it with 'ColourNumberSymbol' on it feels pretty important."""
  #options as to what to do now
    options_dict = {"Open Emails":1, "Open Desk Drawer":1, "Open CCTV History":1, "Leave Room":1}
    global sec_room_completed_dict
    while True:
        #unexplored options record so completed areas won't be displayed again
        unexplored_options = []
        for key in options_dict:
            if options_dict[key] == 1:
                unexplored_options.append(key)
        sec_pc_decision = give_options(unexplored_options)
        if sec_pc_decision == "Leave Room":
            #return to room options menu
            break
        else:
            options_dict[sec_pc_decision] = 0
            output.clear()
            #chose open emails
            if sec_pc_decision == "Open Emails":
                emails_viewed = open_emails()
                #only remove option if all emails viewed
                if emails_viewed < 3:
                    options_dict[sec_pc_decision] = 1
                else:
                    sec_room_completed_dict[sec_pc_decision] = 1
            #chose open desk drawer
            elif sec_pc_decision == "Open Desk Drawer":
                print("""You open the small desk drawer. The only thing in there is a dog-eared
copy of Douglas Adams' book 'The Hitchhikers Guide to the Galaxy.' You pocket the book.\n""")
                case_file["Book seized as Evidence"] = """A copy of 'The Hitchhikers Guide to the Galaxy'
By Douglas Adams. A good read according to Hank's mum."""
                sec_room_completed_dict[sec_pc_decision] = 1
            #chose open CCTV History
            elif sec_pc_decision == "Open CCTV History":
                if b_counter + m_counter + c_counter == 0:
                    print("Hmm a password, maybe Hank's emails will give me a hint.\n")
                password_correct = password_check("red42!")
                if password_correct == True:
                    sec_room_completed_dict[sec_pc_decision] = 1
                    print("""You're in. You scroll back to the time period when the incident must have occurred.
Unfortunately, the camera doesn't point at the fridge, only the door. That seems suspicious in 
itself. Could this have been a premeditated strike? Not being able to see the action is a real setback 
but zooming through the footage does reduce the suspect list significantly. Other than yourself the
only people to enter the kitchenette were Ariyon, David and Sarah.
Their names go in the case file. The noose tightens.\n""")
                    case_file["CCTV_Suspects"] = "Ariyon, David, Sarah."
                else:
                    options_dict[sec_pc_decision] = 1
                    print("""The 'ColourNumberSymbol' post-it seems passwordy, I recon Hank's emails should give me what I need to crack this. 
If I read through them already then I will have taken notes in the case file.\n""")

#Function must be defined after room functions.
#Security Door, takes no arguments, runs controlled entry to security room. If authenticated runs security room function with no output.
#If user does not enter security room, returns give_options string for room to go to. 
#alt riddle: print("""'Its first digit is of no use. Its second and fourth digit is the mirror image of each other.
#The third digit is half the second.'""") - answer: 0848 
def security_door():
    print(f"""You approach the security door, it's locked. There is a number pad, looks like needs a 4 digit code. 
A post-it on the door reads: 
{riddle}""")
    #check if room completed already
    if sum(sec_room_completed_dict.values()) >= 3:
        #kicked back to desk
        print("You have seen(stolen) everything of interest here, check your case file for details.\n")
        next_room = give_options("Return to Desk")
    #check if been here not completed but have passcode
    elif "Security Door Passcode" in case_file:
        #enter security room
        print("You fish around in your pocket, pull out the crumpled post-it with the code and punch it into the keypad.\n")
        next_room = security_room()
    else:
        while True: 
            #ask for passcode
            passcode = numerical_passcode(3, 1, riddle, "3", "1", "4", "1")
            #check if correct
            if passcode == True:
                output.clear()
                #enter security room
                print("The door opens with a click and you walk into the room quickly closing the door behind you.\n")
                case_file["Security Door Passcode"] = "3141"
                next_room = security_room()
                break
            else:
                output.clear()
                print("""'Damn, I'm locked out!' A swift kick to the solid door yields only a sore toe.
Maybe it's time to try your luck elsewhere, as you turn to leave you do notice that 
the numbers 1, 3 and 4 are more worn than the others...\n""")
                #options menu for going to a different room
            while True:
                next_room = give_options("Return to Desk", "Reattempt Security Door")
                if next_room == "Reattempt Security Door":
                    time_check = check_lockout_time(passcode)
                    if time_check == True:
                        print(riddle)    
                        break
                    else:
                        print(f"You have {time_check} remaining of your lockout.\n")
                else:
                    return next_room
    return next_room

security_door()

print_dict(case_file)
