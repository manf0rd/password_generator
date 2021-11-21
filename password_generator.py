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
            if not os.path.exists(os.path.dirname(new_filepath)):
                os.makedirs(os.path.dirname(new_filepath))
            shutil.move(self.filepath, new_filepath)
            print(f'File moved: {new_filepath}')
        except OSError as error:
            print(error)
            print(f'Unable to move: {self.filepath}')
            continue_prompt()

    def delete(self):
        try:
            os.remove(self.filepath)
            print(f'File deleted: {self.filepath}')
        except OSError as error:
            print(error)
            print(f'{self.filepath} can not be removed')
            continue_prompt()

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
            continue_prompt()

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
        exit()

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def exist_menu(root_path,password_file):
    choice = ''
    while choice[:1].lower() not in ['a','o']:
        choice = input('Password file already exists.  (A)rchive existing first or just (O)verwrite?\n')
    match choice:
        case 'a': #archive file
            time_string = time.strftime('%H-%M-%S')
            folder_name = os.path.join(root_path,time.strftime('%Y-%m-%d'))
            new_filepath = os.path.join(folder_name, f'{time_string}_passwords.txt')
            password_file.move(new_filepath)
            password_file.write(password_file.passwords)
            continue_prompt()
        case 'o': #overwrite file
            password_file.write(password_file.passwords)
            continue_prompt()

def main():
    clear_console()
    root_path = 'c:\\temp\\Password_Generator'
    path = input(f'Enter a new export location or press Enter to contine with default - {root_path}\n')
    confirm = ''
    while confirm[:1].lower() != 'y':
        confirm = input(f'Passwords will be written as {os.path.join(path, "passwords.txt")}\nIs this correct? (Y)es or (N)o?\n')
        if confirm[:1].lower() == 'n':
            root_path = 'c:\\temp\\Password_Generator'
            path = input(f'Enter a new export location or press Enter to contine with default - {root_path}\n')
    if not path == '': root_path = path
    while not os.path.isdir(root_path):
        try:
            os.makedirs(root_path)
        except OSError as error:
            print(error)
            print('Please ensure path is entered correctly. Example: c:\\temp\passwords')        
    
    number = input('Enter number of passwords to generate:\n')
    while not number.isdigit():
        number = input('Enter number of passwords to generate:\n')

    password_length = input('Enter password Length:\n')
    while not password_length.isdigit():
        password_length = input('Please provide a number of passwords to generate:\n')
    passwords = [] 

    for i in range(int(number)):
        password = generate_password(int(password_length))
        passwords.append(password)
    
    password_file_path = os.path.join(root_path, 'passwords.txt')
    password_file = file_mover(passwords, password_file_path)

    if os.path.exists(password_file.filepath):
        exist_menu(root_path, password_file)
    else:
        password_file.write(passwords)
    continue_prompt()

if __name__ == '__main__':
    main()