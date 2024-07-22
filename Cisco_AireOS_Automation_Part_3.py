import getpass
from typing import List
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

EXCLUDED_USERNAMES = ['taylor', 'superuser']  # List of usernames to exclude from deletion

def parse_mgmtuser_output(output: str) -> List[str]:
    '''
    Parse the output of the 'show mgmtuser' command and return a list of usernames.

    Parameter output: The output string from the 'show mgmtuser' command
    Return: A list of usernames
    '''
    return [line.split()[0] for line in output.strip().split('\n')[2:]]

def send_command(connection, command: str, confirm: bool = False) -> str:
    '''
    Send a command to the device and optionally confirm it.

    Parameter connection: The Netmiko connection object
    Parameter command: The command to send
    Parameter confirm: Whether to send a confirmation (default: False)
    Return: The output of the command
    '''
    output = connection.send_command_timing(command_string=command)
    if confirm:
        output += connection.send_command_timing(command_string='y', delay_factor=2)
    return output

def main():
    username = input('\nEnter your username: ')
    password = getpass.getpass(prompt='Enter your password: ')

    device = {
        'device_type': 'cisco_wlc',
        'ip': '192.168.10.2',
        'username': username,
        'password': password
    }

    try:
        with ConnectHandler(**device) as net_connect:
            output = send_command(net_connect, 'show mgmtuser')
            usernames = parse_mgmtuser_output(output)

            print(f'\nUsernames found on {device["ip"]}:')
            for username in usernames:
                print(f' - {username}')

            for username in usernames:
                if username not in EXCLUDED_USERNAMES:
                    print(f'\nDeleting user: {username}')
                    send_command(net_connect, f'config mgmtuser delete {username}', confirm=True)
                else:
                    print(f'Skipping user: {username}')

            print('\nChecking configured management users...')
            output = send_command(net_connect, 'show mgmtuser')
            usernames = parse_mgmtuser_output(output)

            print(f'\nUsernames found on {device["ip"]}:')
            for username in usernames:
                print(f' - {username}')

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f'Error connecting to the device: {e}')

if __name__ == '__main__':
    main()