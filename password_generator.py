#! pyton3
import os,random,string,shutil,time
class file_mover:
    def __init__(self, passwords ,filepath):
        self.filepath = filepath
        self.passwords = passwords
        self.new_filepath = filepath
        self.name = os.path.basename(filepath)

    def move(self, new_filepath):
        try:
            shutil.move(self.filepath, new_filepath)
            print(f'File moved:\n\t{new_filepath}')
        except OSError as error:
            print(error)
            print(f'Unable to move {self.filepath}')

    def delete(self):
        try:
            os.remove(self.filepath)
            print(f'File deleted:\n\t{self.filepath}')
        except OSError as error:
            print(error)
            print(f'{self.filepath} can not be removed')

    def write(self,passwords):
        try:
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
            with open(self.filepath, 'w') as file:
                file.write('\n'.join(str(item) for item in passwords))
                print(f'Passwords written to: {self.filepath}')
        except OSError as error:
            print(error)
            print(f'Unable to write {self.filepath}')

def generate_password(password_length=16):
    password = ''
    specials = ['!','@','$','%','^','&','*','<','>','?',';','~',]
    while len(password) < password_length:
        for i in range(2):
            if len(password) < password_length: password += random.choice(string.ascii_lowercase)
            if len(password) < password_length: password += random.choice(string.ascii_uppercase)
            if len(password) < password_length: password += random.choice(string.digits)
            if len(password) < password_length: password += random.choice(specials)
    list_password = list(password)
    random.shuffle(list_password)
    new_password = ''.join(list_password)
    return new_password

def continue_prompt():
    answer = input(f'Would you like to continue? Yes or No?\n')
    answer = answer[:1]
    if answer == 'y':
        main()
    else:
        input('Press any key to close...\n')
        exit()

def exist_menu(root_path,password_file,passwords):
    choice = input('Password file already exists.  Would you like to do (a)rchive first, (o)verwrite, or (r)emove?\n')
    choice = choice[:1]
    if choice not in ['a','o','r']:
        input(f'Password file already exists.  Would you like to do (a)rchive first, (o)verwrite, or (r)emove?\n')
    match choice:
        case 'a': #archive file
            timestr = time.strftime("%Y%m%d-%H%M")
            new_filepath = os.path.join(root_path,'archive',f'{timestr}_passwords.txt')
            password_file.move(new_filepath)
            password_file.write(passwords)
            continue_prompt()
        case 'o': #overwrite file
            password_file.delete()
            password_file.write(passwords)
            continue_prompt()
        case 'r': #delete file
            password_file.delete()
            continue_prompt()
        case _:
            print("None valid input\n")
            continue_prompt(exist_menu(root_path,password_file,passwords))

def main():
    default_root_path = 'c:\\temp\\Password_Generator'
    path = input(f'Default save location is: {default_root_path}\nEnter a new path or press Enter to contine with default.\n')

    if not path == '':
        root_path = os.path.expanduser(path)
        while not os.path.exists(root_path):
            try:
                os.mkdir(root_path)
            except OSError as error:
                print(error)
                print(f'Please ensure path is entered correctly. Example: c:\\temp\passwords')
    root_path = default_root_path
    
    number = input('Enter number of passwords to generate:\n')
    while not number.isdigit():
        number = input(f'Enter number of passwords to generate:\n')

    password_length = input('Enter password Length:\n')
    while not password_length.isdigit():
        password_length = input(f'Please provide a number of passwords to generate:\n')
    passwords = [] 

    for i in range(int(number)):
        password = generate_password(int(password_length))
        passwords.append(password)
    
    password_file_path = os.path.join(root_path, 'passwords.txt')
    password_file = file_mover(passwords, password_file_path)

    if os.path.exists(password_file.filepath):
        exist_menu(root_path, password_file, passwords)
    else:
        password_file.write(passwords)
    continue_prompt()

if __name__ == '__main__':
    main()


#TODO add default c:\temp\password_generator\day_month\passwords_date.txt, change file path option