import pandas

# Read the CSV into a DataFrame
data = pandas.read_csv(r"C:\Users\meet\OneDrive\Desktop\MEET\Pandas Project\NATO ALPHABET PROJECT\nato_phonetic_alphabet.csv")

# ✅ Create a dictionary from the DataFrame
data_dictionary = {row.letter: row.code for (index, row) in data.iterrows()}

def generate_phonetic():
    # ✅ Create a list of the phonetic code words from the user input

    word = input("Enter a word: ").upper()
    try:
        output_list = [data_dictionary[letter] for letter in word]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic()
    else:
        print(output_list)
