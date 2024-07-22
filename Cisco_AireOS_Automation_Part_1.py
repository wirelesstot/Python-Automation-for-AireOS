from netmiko import ConnectHandler  # Import the ConnectHandler factory function that will handle the SSH connection to the device

# Anything between three single quotes is a multi-line comment. It's useful for writing longer comments.
'''
Set your device connection details. This is a dictionary that contains the device's IP address, username, and password.
Each key in the dictionary is on a new line and indented with 4 spaces (1 tab) for readability. You can put them all
on one line if you want, but it's harder to read. Make sure each entry in the dictionary has a comma at the end to separate
each key-value pair. The keys are strings, so they're in single quotes. The values are also strings, so they're in single
quotes too. The dictionary is assigned to the variable 'device'. The dictionary is a data structure that stores key-value
pairs. In this case, the keys are 'device_type', 'ip', 'username', and 'password', and the values are 'cisco_wlc', 
'192.168.11.12', 'admin', and 'totallynotadmin'.
'''
device = {
    'device_type': 'cisco_wlc',  # Set device type as 'cisco_wlc', which for Netmiko is AireOS-based WLCs (not IOS-XE)
    'ip': '192.168.11.12',  # Your device's IP address
    'username': 'admin',  # Your device's SSH username
    'password': 'totallynotadmin'  # Your device's SSH password
}
# Establish an SSH connection to the device using the device dictionary:
net_connect = ConnectHandler(**device)

# Send some commands to the device and print the output:
output = net_connect.send_command(command_string='show wlan summary')
print(output)

# Disconnect from the device:
net_connect.disconnect()
