from os import system, path

# Python
system("sudo apt install python3.7")
system("sudo apt install python3-pip")

# Libraries
system("sudo pip3 install python-dotenv")
system("sudo pip3 install RPi.GPIO")
system("sudo pip3 install Pillow")
system(f"sudo cp -r {path.join(path.dirname(__file__), 'waveshare_epd')} /lib/python3.7")

# Setup Part 2
system(f"sudo python3.7 {path.join(path.dirname(__file__), 'setup3.7.py')}")

# End Message
print("Setup End")
print("Please install BCM2835 and wiring PI, instructions here : https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT")
print("Once installed start the service with the command : sudo systemctl start hardware.service")