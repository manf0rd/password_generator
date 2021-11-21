#! pyton3

import random,os,string

def out_file(filepath, new_passwords):
    try:
        with open(filepath, "w") as file:
            file.write("\n".join(str(item) for item in new_passwords))
    except:
        print("Unable to write to path")

def generate_password(password_length):
    password = ''
    specials = ['!','@','$','%','^','&','*','<','>','?',';','~',]
    while len(password) < password_length:
        for i in range(2):
            password += random.choice(string.ascii_lowercase)
            password += random.choice(string.ascii_uppercase)
            password += random.choice(string.digits)
            password += random.choice(string.punctuation)
            password += random.choice(specials)
    list_password = list(password)
    random.shuffle(list_password)
    new_password = ''.join(list_password)
    return new_password

def main():
    filepath = "/workspace/Projects/passwords.txt"
    if os.path.exists(filepath):
        os.remove(filepath)
    print('Password Generator'.center(os.get_terminal_size().columns)+"\n")
    print('Enter passwords to generate:')
    number = int(input())
    print('Enter password Length:')
    password_length = int(input())

    passwords = []

    for i in range(number):
        passwords.append(generate_password(password_length))
        
    print('Passwords:')
    for i in passwords:
        print(i)
    
    out_file(filepath, passwords)
    print(f'Exported to: {filepath}')

if __name__ == '__main__':
    main()