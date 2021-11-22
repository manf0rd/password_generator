#! python3
#TODO add import csv support, Config.ini
import os, random, shutil, subprocess, time
from string import ascii_lowercase as lowercase_in_password, ascii_uppercase as uppercase_in_password, digits as digits_in_password

def clip_text(text):
	subprocess.run(['clip.exe'], input=text.strip().encode('utf-16'), check=True)

def build_password_generator_configuration(configuration_dict={}):
	default_password_generator_configuration = {
		'number_of_passwords' : 1, 'password_length' : 16, 'digits_in_password' : 2,
		'uppercase_in_password' : 2, 'lowercase_in_password' : 2, 'specials_in_password' : 2
		}
	if configuration_dict.keys() != default_password_generator_configuration.keys():
		configuration_dict = default_password_generator_configuration
		
	print('Current Password Generator Configuration:\n')
	for item in configuration_dict:
		print(f'{item.upper()} : {configuration_dict[item]}')
	property_to_change = input(f'\nEnter property name to change or press Enter to continue with current configuration:\n')

	if property_to_change != '' and property_to_change in configuration_dict.keys():
		value = int(input(f'New value for {property_to_change}:\n'))		
		if not value >= 1:
			value = input(f'Value must be a number.  Type new value for {property_to_change} or press Enter to abort:\n')
		else:
			configuration_dict[property_to_change] = value
			build_password_generator_configuration(configuration_dict)

	elif property_to_change != '':
		print(f'{property_to_change} is not a valid property\nPlease ensure that what you type matches one of the following:\n')
		for i in configuration_dict.keys:
			print(i)
		build_password_generator_configuration(default_password_generator_configuration)

	sum_of_complexity = int(configuration_dict['digits_in_password']) + int(configuration_dict['uppercase_in_password']) + int(configuration_dict['lowercase_in_password']) + int(configuration_dict['specials_in_password'])
	if sum_of_complexity > configuration_dict['password_length']:
		print('Invalid configuration:\nNumber of required characters is greater than password length\n')
		build_password_generator_configuration(default_password_generator_configuration)
		return build_password_generator_configuration(configuration_dict)
	return configuration_dict

def password_generator(password_configuration_dict):
	new_password = ''
	specials_in_password = ['!','@','$','%','^','&','*','<','>','?',';','~',]
	password_complexity = [uppercase_in_password, lowercase_in_password, digits_in_password, specials_in_password]
	while len(new_password) < password_configuration_dict['password_length']:
		for item in password_complexity:
			if len(new_password) < password_configuration_dict['password_length']:
				new_password += random.choice(item)
	return new_password	

def save_file(passwords):
	filepath = 'c:\\Temp\\Password_Generator\\passwords.txt'
	change_name = yes_no_prompt(f'Default save location is: {filepath}\nWould you like to change it?')
	if change_name:
		passworld_file = input('Enter new file path to save to: (c:\\temp\\passwords.txt)\n')
	else:
		password_file = filepath

	try:
		if os.path.exists(password_file):
			archive_file = yes_no_prompt('File already exists. Would you like to archive before saving?')
			if archive_file:
				time_string = time.strftime('%H-%M-%S')
				folder_name = os.path.join(os.path.dirname(password_file),time.strftime('%Y-%m-%d'))
				old_password_file = os.path.join(folder_name, f'{time_string}_passwords.txt')
				try:
					if not os.path.exists(folder_name):
						try:
							os.makedirs(folder_name)
						except OSError as error:
							print(error)
							print('Unable to create archive directory')
					shutil.move(password_file, old_password_file)
					print(f'Archive file moved:{old_password_file}')
					new_file = open(password_file, 'x')
					new_file.write(passwords)
					new_file.close()
					print(f'Created new file: {password_file}')
				except OSError as error:
					print(error)
					print('Failed to archive')
			else:
				try:
					file = open(password_file, 'w')
					file.write(passwords)
					file.close()
					print(f'File overwritten: {password_file}')
				except OSError as error:
					print(error)
					print('Failed to overwrite')
		else:
			if not os.path.exists(os.path.dirname(password_file)):
				try:
					os.makedirs(os.path.dirname(password_file))
					file = open(password_file, 'x')
					file.write(passwords)
					file.close()
					print(f'File and directories created: {password_file}')
				except OSError as error:
					print(error)
					print('Failed to write new file')
			else:
				try:
					file = open(password_file, 'x')
					file.write(passwords)
					file.close()
					print(f'New file created: {password_file}')
				except OSError as error:
					print(error)
					print('Failed to write new file')
	except OSError as error:
		print(error)
		print('Failed to save')

def yes_no_prompt(option=''):
	to_continue = 'Would you like to continue?'
	answer = input(f'{option if option else to_continue}\n')
	return True if answer[:1].lower() == 'y' else False

def main():
	password_configuration = build_password_generator_configuration()	
	if password_configuration['number_of_passwords'] > 1:
		password_list = ''
		for i in range(password_configuration['number_of_passwords']):
			password_list += f'{password_generator(password_configuration)}\n'		
		print(f'New Passwords:\n\n{password_list}')
		print('\nPasswords also copied to clipboard')
		clip_text(password_list)
		choice = yes_no_prompt('Would you like to save the passwords to file?')
		if choice:
			save_file(password_list)

	else:
		new_password = password_generator(password_configuration)
		print(f'New Password\n{new_password}')
		print('\nPassword also copied to clipboard')
		clip_text(new_password)
		choice = yes_no_prompt('Would you like to save the passwords to file?')
		if choice:
			save_file(new_password)

	main() if yes_no_prompt() else exit()

if __name__ == '__main__':
	main()