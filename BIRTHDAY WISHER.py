import smtplib
import datetime as dt
import csv

# 📅 Get today's date
now = dt.datetime.now()
today_day = now.day
today_month = now.month

# 📁 CSV file location
csv_file = r"C:\Users\meet\OneDrive\Desktop\MEET\Email Projects\Birthday Wisher\bithday.csv"

# 📧 Email settings
my_email = "meetmalpani9b.school@gmail.com"
password = "awaiwwidcjzyqoob"  # ⚠️ Use Gmail App Password

# 🎂 Common birthday message (with {name} placeholder)
birthday_message = """Subject: Happy Birthday {name}! 🎂🎉

Hey {name}! 🎈

Happy Birthday, bhaii!! 🎁
Hope your day is:
🍰 Full of cake
🎮 Packed with fun
😂 Loaded with laughter
✨ Magical in every way

Happpy Bday!!! Let's party soon! 🥳

Best wishes,
Meet"""

# 📖 Read CSV and find today's birthdays
birthday_people = []

try:
    with open(csv_file, encoding="utf-8") as file:
        data = csv.DictReader(file)
        
        for row in data:
            name = row['name']
            email = row['email']
            dob = row['dob']  # Format: DD/MM/YYYY
            
            # Extract day and month from DOB
            dob_parts = dob.split('/')
            dob_day = int(dob_parts[0])
            dob_month = int(dob_parts[1])
            
            # ✅ Step 2: Check if today matches a birthday
            if dob_day == today_day and dob_month == today_month:
                birthday_people.append({'name': name, 'email': email})

    # ✅ Step 4: Send email to each birthday person
    if birthday_people:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            
            for person in birthday_people:
                # Personalize message with their name
                message = birthday_message.format(name=person['name'])
                
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=person['email'],
                    msg=message
                )
                print(f"✅ Sent to {person['name']} ({person['email']})")
        
        print(f"\n🎉 Total emails sent: {len(birthday_people)}")
    else:
        print("📭 No birthdays today!")

except FileNotFoundError:
    print(f"❌ CSV file not found: {csv_file}")
except Exception as e:
    print(f"❌ Error: {e}")
