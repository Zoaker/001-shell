#1.  modify python and ubuntu mirrors 
sudo cp -rf .pip  ~/.pip
sudo cp ./bash/ubuntu/sources.list /etc/opt/sources.list

#2. modify windows wsl config
sudo cp ./bash/ubuntu/wsl.conf /etc/wsl.conf

#3. install gvim
cd ~/
sudo apt-get install vim-gnome

#4. install pyqt5
sudo python3 -m pip install --upgrade pip
sudo pip3 install pyqt5==5.12.0
sudo apt install pyqt5*
sudo apt install qt5-default qttools5-dev-tools
