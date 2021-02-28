from os import system, path, getenv

# Python
system("sudo apt install python3.7")
system("sudo apt install python3-pip")

# Libraries
system("sudo pip3 install python-dotenv")
system("sudo pip3 install RPi.GPIO")
system("sudo pip3 install Pillow")
system(f"sudo cp -r {path.join(path.dirname(__file__), 'waveshare_epd')} /lib/python3.7")

# Environment variables
from dotenv import load_dotenv
load_dotenv(path.join(path.dirname(__file__), '.env'))

# Hardware Files
system(f"sudo cp {path.join(path.dirname(__file__), 'src/.env')} {path.join(getenv('INSTALL_DIR'), '.env')}")
system(f"sudo cp {path.join(path.dirname(__file__), 'src/Font.ttc')} {path.join(getenv('INSTALL_DIR'), 'Font.ttc')}")
system(f"sudo cp {path.join(path.dirname(__file__), 'src/hardware.log')} {path.join(getenv('INSTALL_DIR'), 'hardware.log')}")
system(f"sudo cp {path.join(path.dirname(__file__), 'src/hardware.py')} {path.join(getenv('INSTALL_DIR'), 'hardware.py')}")

# Hardware as a service
hardware_service_content = f"[Unit]\nDescription=Control of the pi by hardware\nAfter=network.target\n\n[Service]\nType=simple\nRestart=on-failure\nExecStart=/usr/bin/python3.7 {path.join(getenv('INSTALL_DIR'), 'hardware.py')}\n\n[Install]\nWantedBy=multi-user.target"
hardware_service_file = open("/etc/systemd/system/hardware.service", "w")
hardware_service_file.write(hardware_service_content)
hardware_service_file.close()
system("sudo systemctl daemon-reload")
system("sudo systemctl enable hardware.service")

print("Setup End")
print("Please install BCM2835 and wiring Pi")
print("According to this link: https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT")
print("Once installed start the service with the command 'sudo systemctl start hardware.service'")
