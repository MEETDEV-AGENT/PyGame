import random

# HIGHER LOWER GAME
# ASCII Art for Higher Lower
higher_lower = """
                   $$\   $$\ $$$$$$\  $$$$$$\  $$\   $$\ $$$$$$$$\ $$$$$$$\  
                   $$ |  $$ |\_$$  _|$$  __$$\ $$ |  $$ |$$  _____|$$  __$$\ 
                   $$ |  $$ |  $$ |  $$ /  \__|$$ |  $$ |$$ |      $$ |  $$ |
                   $$$$$$$$ |  $$ |  $$ |$$$$\ $$$$$$$$ |$$$$$\    $$$$$$$  |
                   $$  __$$ |  $$ |  $$ |\_$$ |$$  __$$ |$$  __|   $$  __$$< 
                   $$ |  $$ |  $$ |  $$ |  $$ |$$ |  $$ |$$ |      $$ |  $$ |
                   $$ |  $$ |$$$$$$\ \$$$$$$  |$$ |  $$ |$$$$$$$$\ $$ |  $$ |
                   \__|  \__|\______| \______/ \__|  \__|\________|\__|  \__|
                                                          
                    $$\       $$$$$$\  $$\      $$\ $$$$$$$$\ $$$$$$$\        
                    $$ |     $$  __$$\ $$ | $\  $$ |$$  _____|$$  __$$\       
                    $$ |     $$ /  $$ |$$ |$$$\ $$ |$$ |      $$ |  $$ |      
                    $$ |     $$ |  $$ |$$ $$ $$\$$ |$$$$$\    $$$$$$$  |      
                    $$ |     $$ |  $$ |$$$$  _$$$$ |$$  __|   $$  __$$<       
                    $$ |     $$ |  $$ |$$$  / \$$$ |$$ |      $$ |  $$ |      
                    $$$$$$$$\ $$$$$$  |$$  /   \$$ |$$$$$$$$\ $$ |  $$ |      
                    \________|\______/ \__/     \__|\________|\__|  \__|                                     
                                                                                                               
                                                          
"""

# ASCII Art for VS
vs = """
        $$\    $$\  $$$$$$\\
        $$ |   $$ |$$  __$$\\ 
        $$ |   $$ |$$ /  \\__|
        \\$$\  $$  |\\$$$$$$\ 
         \\$$\$$  /  \\____$$\ 
          \\$$$  /  $$\   $$ |
           \\$  /   \\$$$$$$  |
            \\_/     \\______/
"""

# Giving sufficient data for the computer to execcute the game smoothly
data = [
    {
        'name': 'Instagram',
        'follower_count': 346,
        'description': 'Social media platform',
        'country': 'United States'
    },
    {
        'name': 'Cristiano Ronaldo',
        'follower_count': 215,
        'description': 'Footballer',
        'country': 'Portugal'
    },
    {
        'name': 'Ariana Grande',
        'follower_count': 183,
        'description': 'Musician and actress',
        'country': 'United States'
    },
    {
        'name': 'Dwayne Johnson',
        'follower_count': 181,
        'description': 'Actor and professional wrestler',
        'country': 'United States'
    },
    {
        'name': 'Selena Gomez',
        'follower_count': 174,
        'description': 'Musician and actress',
        'country': 'United States'
    },
    {
        'name': 'Kylie Jenner',
        'follower_count': 173,
        'description': 'Entrepreneur and influencer',
        'country': 'United States'
    },
    {
        'name': 'Lionel Messi',
        'follower_count': 168,
        'description': 'Footballer',
        'country': 'Argentina'
    },
    {
        'name': 'Kim Kardashian',
        'follower_count': 160,
        'description': 'Reality TV star and entrepreneur',
        'country': 'United States'
    },
    {
        'name': 'Beyoncé',
        'follower_count': 150,
        'description': 'Singer and businesswoman',
        'country': 'United States'
    },
    {
        'name': 'Justin Bieber',
        'follower_count': 145,
        'description': 'Musician',
        'country': 'Canada'
    },
    {
        'name': 'Taylor Swift',
        'follower_count': 140,
        'description': 'Singer and songwriter',
        'country': 'United States'
    },
    {
        'name': 'Neymar',
        'follower_count': 138,
        'description': 'Footballer',
        'country': 'Brazil'
    },
    {
        'name': 'Kendall Jenner',
        'follower_count': 130,
        'description': 'Model and influencer',
        'country': 'United States'
    },
    {
        'name': 'National Geographic',
        'follower_count': 120,
        'description': 'Educational media',
        'country': 'United States'
    },
    {
        'name': 'Nike',
        'follower_count': 118,
        'description': 'Sports brand',
        'country': 'United States'
    },
    {
        'name': 'Jennifer Lopez',
        'follower_count': 112,
        'description': 'Singer and actress',
        'country': 'United States'
    },
    {
        'name': 'Virat Kohli',
        'follower_count': 108,
        'description': 'Cricketer',
        'country': 'India'
    },
    {
        'name': 'Khloé Kardashian',
        'follower_count': 105,
        'description': 'Reality TV star',
        'country': 'United States'
    },
    {
        'name': 'Shakira',
        'follower_count': 102,
        'description': 'Singer and performer',
        'country': 'Colombia'
    },
    {
        'name': 'Drake',
        'follower_count': 100,
        'description': 'Rapper and singer',
        'country': 'Canada'
    },
    {
        'name': 'Billie Eilish',
        'follower_count': 95,
        'description': 'Singer and songwriter',
        'country': 'United States'
    },
    {
        'name': 'LeBron James',
        'follower_count': 92,
        'description': 'Basketball player',
        'country': 'United States'
    },
    {
        'name': 'Real Madrid',
        'follower_count': 90,
        'description': 'Football club',
        'country': 'Spain'
    },
    {
        'name': 'FC Barcelona',
        'follower_count': 88,
        'description': 'Football club',
        'country': 'Spain'
    },
    {
        'name': 'Chris Hemsworth',
        'follower_count': 86,
        'description': 'Actor',
        'country': 'Australia'
    },
    {
        'name': 'NASA',
        'follower_count': 84,
        'description': 'Space agency',
        'country': 'United States'
    },
    {
        'name': 'Zendaya',
        'follower_count': 82,
        'description': 'Actress and singer',
        'country': 'United States'
    },
    {
        'name': 'Shawn Mendes',
        'follower_count': 80,
        'description': 'Singer and songwriter',
        'country': 'Canada'
    },
    {
        'name': 'Conor McGregor',
        'follower_count': 78,
        'description': 'MMA fighter',
        'country': 'Ireland'
    },
    {
        'name': 'Vin Diesel',
        'follower_count': 76,
        'description': 'Actor',
        'country': 'United States'
    },
    {
        'name': 'Emma Watson',
        'follower_count': 74,
        'description': 'Actress and activist',
        'country': 'United Kingdom'
    },
    {
        'name': 'Robert Downey Jr.',
        'follower_count': 72,
        'description': 'Actor',
        'country': 'United States'
    },
    {
        'name': 'Camila Cabello',
        'follower_count': 70,
        'description': 'Singer and songwriter',
        'country': 'United States'
    },
    {
        'name': 'Miley Cyrus',
        'follower_count': 68,
        'description': 'Singer and actress',
        'country': 'United States'
    }
]

# Function to format data
def format_data(account):
    """Format the account data into a printable format."""
    account_name = account["name"]
    account_description = account["description"]
    account_place = account["country"]
    return f"{account_name}, a {account_description}, from {account_place}"

def check_answer(user_guess, a_follower, b_follower):
    """Take the user's guess and the follower count of both accounts, then return if they are correct."""
    if a_follower > b_follower:
        return user_guess == 'A'
    else:
        return user_guess == 'B'

def higher_lower_game():
    """Main function to run the Higher Lower game."""
    print(higher_lower)
    score = 0
    game_should_continue = True
    account_b = random.choice(data)  # Selecting a random account for comparison

    # Making the game repeatable
    while game_should_continue:
        account_a = account_b
        account_b = random.choice(data)
        # Generating two different random accounts
        while account_a == account_b:
            account_b = random.choice(data)  # Ensure account_b is different from account_a
        # Printing the formatted data
        print(f"Compare A: {format_data(account_a)}")
        print(vs)
        print(f"Against B: {format_data(account_b)}")
        # Ask user for a guess
        user_guess = input("Who has more followers? Type 'A' or 'B': ").strip().upper()

        # Checck if user is correct
        # - Get follower count form each account
        a_follower_count = account_a["follower_count"]
        b_follower_count = account_b["follower_count"]
        # - Use if statement to check if the user is correct
        is_correct = check_answer(user_guess, a_follower_count, b_follower_count)
        
        # Give user feedback on their guess
        if is_correct:
            # Score keeping
            print("\n" * 100)
            score += 1
            print(f"You're right! Current score: {score}")
            print(higher_lower)
        else:
            print(f"Sorry, that's wrong. Final score: {score}")
            print("Refresh the page to try again.")
            game_should_continue = False

higher_lower_game()
 
