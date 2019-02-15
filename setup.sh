#/bin/bash

echo "Starting setup..."
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi
echo "Installing pip..."
if  [-x "$(command -v pip)" ]; then
    echo "pip already installed... moving on.."
else
    easy_install pip
fi
echo "Installing packages..."
sudo pip install Pillow
sudo pip install requests
sudo pip install pathlib

echo "All done! :)"


