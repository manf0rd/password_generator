#! pyton3
#TODO add default c:\temp\password_generator\day_month\passwords_date.txt, change file path option
import os,random,string,shutil,time
from colorama import Fore, Style

root_path = 'c:\\temp'
class file_mover:
    def __init__(self, passwords ,filepath):
        self.filepath = filepath
        self.passwords = passwords
        self.new_filepath = filepath
        self.name = os.path.basename(filepath)

    def move(self, new_filepath):
        try:
            shutil.move(self.filepath, new_filepath)
            print(f'{Fore.GREEN}File moved:\n\t{new_filepath}{Style.RESET_ALL}')
        except OSError as error:
            print(error)
            print(f'{Fore.RED}Unable to move {self.filepath}{Style.RESET_ALL}')

    def delete(self):
        try:
            os.remove(self.filepath)
            print(f'{Fore.GREEN}File deleted:\n\t{self.filepath}{Style.RESET_ALL}')
        except OSError as error:
            print(error)
            print(f'{Fore.RED}{self.filepath} can not be removed{Style.RESET_ALL}')

    def write(self,passwords):
        try:
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
            with open(self.filepath, 'w') as file:
                file.write('\n'.join(str(item) for item in passwords))
                print(f'{Fore.GREEN}Passwords written to: {self.filepath}{Style.RESET_ALL}')
        except OSError as error:
            print(error)
            print(f'{Fore.RED}except to write{Style.RESET_ALL}')

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
    answer = input(f'{Fore.YELLOW}Would you like to continue? Yes or No?{Style.RESET_ALL}\n')
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
        input(f'{Fore.RED}Password file already exists.  Would you like to do (a)rchive first, (o)verwrite, or (r)emove?{Style.RESET_ALL}\n')
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
    try:
        if not os.path.exists(root_path):
            os.mkdir(root_path)
    except OSError as error:
        print(error)
        print(f'{Fore.RED}Unable to create temp directory{Style.RESET_ALL}')
        continue_prompt()

    number = input('Enter number of passwords to generate:\n')
    while not number.isdigit():
        number = input(f'{Fore.RED}Enter number of passwords to generate:{Style.RESET_ALL}\n')

    password_length = input('Enter password Length:\n')
    while not password_length.isdigit():
        password_length = input(f'{Fore.RED}Please provide a number of passwords to generate:{Style.RESET_ALL}\n')
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