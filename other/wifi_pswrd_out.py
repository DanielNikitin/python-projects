import subprocess


def extract_wifi_passwords():
    """Extracts Windows Wi-Fi passwords into .txt file"""

    profiles_data = subprocess.check_output('netsh wlan show profiles').decode('utf-8').split('\n')
    profiles = [i.split(':')[1].strip() for i in profiles_data if 'All User Profile' in i]

    for profile in profiles:
        try:
            profile_info = subprocess.check_output(f'netsh wlan show profile "{profile}" key=clear').decode('utf-8').split('\n')
            password = [i.split(':')[1].strip() for i in profile_info if 'Key Content' in i][0]
        except Exception as e:
            print(f'Could not retrieve password for {profile}: {e}')
            password = None

        if password is not None:
            with open(file='wifi_passwords.txt', mode='a', encoding='utf-8') as file:
                file.write(f'Profile: {profile}\nPassword: {password}\n{"#" * 20}\n')
        else:
            print(f'Skipping {profile}, no password could be retrieved')


def main():
    extract_wifi_passwords()


if __name__ == '__main__':
    main()