# Treasure Hunt Game
# ASCII ART
art_treasure = """                            
  *   ) )\ )       (      )\ )        )\ )       ( /(         ( /(   *   )  
` )  /((()/( (     )\    (()/(    (  (()/( (     )\())    (   )\())` )  /(  
 ( )(_))/(_)))\ ((((_)(   /(_))   )\  /(_)))\   ((_)\     )\ ((_)\  ( )(_)) 
(_(_())(_)) ((_) )\ _ )\ (_))  _ ((_)(_)) ((_)   _((_) _ ((_) _((_)(_(_())  
|_   _|| _ \| __|(_)_\(_)/ __|| | | || _ \| __| | || || | | || \| ||_   _|  
  | |  |   /| _|  / _ \  \__ \| |_| ||   /| _|  | __ || |_| || .` |  | |    
  |_|  |_|_\|___|/_/ \_\ |___/ \___/ |_|_\|___| |_||_| \___/ |_|\_|  |_|    
                                                                            """
print(art_treasure)

print("🏝️ Welcome to the Ultimate Treasure Hunt Adventure!")
print("Your mission is to find the treasure and escape alive. Let's begin...")

# First scenario: Classic crossroad
road_choice = input("\nYou're at a crossroad. Where do you want to go? Type 'left' or 'right': ").lower()

if road_choice == "left":
    choice1 = input("\nYou come to a lake. There's an island in the middle of the lake.\nType 'wait' to wait for a boat or 'swim' to swim across: ").lower()
    if choice1 == "wait":
        print("\nNice! You waited and safely reached the island.")
        
        door_choice = input("\nYou find a house with 3 doors: one 'red', one 'yellow', and one 'blue'. Which color do you choose? ").lower()
        
        if door_choice == "red":
            print("\n🔥 Oh no! The room catches fire. Game Over!")
        elif door_choice == "blue":
            print("\n🐉 A giant beast devours you. Game Over!")
        elif door_choice == "yellow":
            print("\n🎉 You found the treasure! But... a final test awaits to truly win...")

            # Add the Treasure Caves Puzzle here
            print("\nYou see two mysterious caves now:")
            print("🖤 Black Door: 'Monster is here.'")
            print("🤎 Brown Door: 'Only one door speaks the truth.'")

            cave_choice = input("Which door do you choose to enter? Type 'black' or 'brown': ").lower()

            # Puzzle logic:
            # If Black Door is true (monster is there), Brown must be false (both cannot be true).
            # If Black Door is false (no monster), Brown is true.
            # Correct answer is to choose the Brown Door for safety.
            if cave_choice == "brown":
                print("\n✅ Smart choice! You figured out the logic puzzle and move ahead safely.")
                
                # Add the Final Escape Puzzle
                print("\nBut wait! A final escape challenge blocks your way.")
                print("You're in a room with 3 doors:")
                print("1️⃣ Door 1: A lake filled with deadly crocodiles.")
                print("2️⃣ Door 2: An angry person with a weapon.")
                print("3️⃣ Door 3: A tiger that hasn’t eaten in 3 months.")

                final_choice = input("Which door do you choose to escape? Type '1', '2', or '3': ")

                if final_choice == "3":
                    print(r'''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\ ` . "-._ /_______________|_______
|                   | |o ;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
''')
                    print("\n🎯 Brilliant! The tiger is dead after 3 months of no food. You escape and truly WIN the game! 🏆🎉")
                else:
                    art_game_over = """                   *              )               (     
 (        (      (  `          ( /(               )\ )  
 )\ )     )\     )\))(   (     )\()) (   (   (   (()/(  
(()/(  ((((_)(  ((_)()\  )\   ((_)\  )\  )\  )\   /(_)) 
 /(_))_ )\ _ )\ (_()((_)((_)    ((_)((_)((_)((_) (_))   
(_)) __|(_)_\(_)|  \/  || __|  / _ \\ \ / / | __|| _ \  
  | (_ | / _ \  | |\/| || _|  | (_) |\ V /  | _| |   /  
   \___|/_/ \_\ |_|  |_||___|  \___/  \_/   |___||_|_\  """
                    print(art_game_over)
                    print("\n💥 Oops! That was a deadly choice. Game Over!")

            else:
                art_game_over = """
    
 (        (      (  `          ( /(               )\ )  
 )\ )     )\     )\))(   (     )\()) (   (   (   (()/(  
(()/(  ((((_)(  ((_)()\  )\   ((_)\  )\  )\  )\   /(_)) 
 /(_))_ )\ _ )\ (_()((_)((_)    ((_)((_)((_)((_) (_))   
(_)) __|(_)_\(_)|  \/  || __|  / _ \\ \ / / | __|| _ \  
  | (_ | / _ \  | |\/| || _|  | (_) |\ V /  | _| |   /  
   \___|/_/ \_\ |_|  |_||___|  \___/  \_/   |___||_|_\  """
                print(art_game_over)
                print("\n💀 The monster was waiting! You fell into the trap. Game Over!")

        else:
            art_game_over = """
                                    
 (        (      (  `          ( /(               )\ )  
 )\ )     )\     )\))(   (     )\()) (   (   (   (()/(  
(()/(  ((((_)(  ((_)()\  )\   ((_)\  )\  )\  )\   /(_)) 
 /(_))_ )\ _ )\ (_()((_)((_)    ((_)((_)((_)((_) (_))   
(_)) __|(_)_\(_)|  \/  || __|  / _ \\ \ / / | __|| _ \  
  | (_ | / _ \  | |\/| || _|  | (_) |\ V /  | _| |   /  
   \___|/_/ \_\ |_|  |_||___|  \___/  \_/   |___||_|_\  
                                                        """
            print(art_game_over)
            print("\n😈 Invalid choice! You are sucked into a dark void. Game Over!")

    else:
        art_game_over = """
                       
 (        (      (  `          ( /(               )\ )  
 )\ )     )\     )\))(   (     )\()) (   (   (   (()/(  
(()/(  ((((_)(  ((_)()\  )\   ((_)\  )\  )\  )\   /(_)) 
 /(_))_ )\ _ )\ (_()((_)((_)    ((_)((_)((_)((_) (_))   
(_)) __|(_)_\(_)|  \/  || __|  / _ \\ \ / / | __|| _ \  
  | (_ | / _ \  | |\/| || _|  | (_) |\ V /  | _| |   /  
   \___|/_/ \_\ |_|  |_||___|  \___/  \_/   |___||_|_\  
                                                        """
        print(art_game_over)
        print("\n🐟 You tried to swim but were attacked by a trout. Game Over!")

else:
    art_game_over = """
                   *              )               (     
 (        (      (  `          ( /(               )\ )  
 )\ )     )\     )\))(   (     )\()) (   (   (   (()/(  
(()/(  ((((_)(  ((_)()\  )\   ((_)\  )\  )\  )\   /(_)) 
 /(_))_ )\ _ )\ (_()((_)((_)    ((_)((_)((_)((_) (_))   
(_)) __|(_)_\(_)|  \/  || __|  / _ \\ \ / / | __|| _ \  
  | (_ | / _ \  | |\/| || _|  | (_) |\ V /  | _| |   /  
   \___|/_/ \_\ |_|  |_||___|  \___/  \_/   |___||_|_\  
                                                        """
    print(art_game_over)
    print("\n💥 Wrong way! You fell into a deep hole. Game Over!")
