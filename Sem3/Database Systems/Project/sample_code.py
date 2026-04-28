import os

def safe_function():
    print("Hello, world!")

def vulnerable_function(user_input):
    eval(user_input)  # dangerous
    os.system("ls")   # dangerous

def main():
    user_input = input("Enter command: ")
    vulnerable_function(user_input)
