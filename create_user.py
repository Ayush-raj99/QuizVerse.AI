from database import create_database, add_user


# Make sure database exists
create_database()


print("================================")
print("     QuizVerse AI User Creator")
print("================================")


username = input("Enter username: ")
password = input("Enter password: ")


success, message = add_user(username, password)


print()
print(message)