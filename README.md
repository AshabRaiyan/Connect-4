# Connect 4 🎮

A simple 2-player Connect 4 game built using **Python**, **Kivy**, and **KivyMD**.

##  About the Game
A classic Connect 4 implementation with a touch-friendly UI designed using **Kivy** and **KivyMD**, making it suitable for both desktop and mobile environments.

## Features
- 6x7 game board
- Graphical user interface using Kivy and KivyMD
- Win condition detection for all possible cases
- Restart button to restart at any time.
- Visual turn indication using a green circle to denote the turn of player


## GUI
The GUI is ****very**** simple (pictures below). I didn't try to make the homepage or game screen nicer when I was making this app. I may do this in future.
When the app starts the window will resize. It might look slim but I set this so that I can test the UI properly before making it into an apk for my phone.



main.py and Connect4.kv file contains all the required code. Assets folder contains the required pictures for Android APK, including the icon and presplash. 
Presplash and icon are only shown on the APK. These aren't shown when running it on dekstop.

## Dependencies:
I used Python 3.12, Kivy 2.3.0 and KivyMD 1.2.0. 
I haven't tested the app using latest version of python and kivy. So it may not work with future versions if some tools get deprecated. So make sure you have these installed.

## How to Run
To run this, make sure you put the **Assets** and **Connect4.kv** file on the same folder as **main.py** file. Then run the main file.

## Pictures from Game
![image](https://github.com/user-attachments/assets/c266bc16-fbe5-4a32-8017-8f79676e149a) ![image](https://github.com/user-attachments/assets/dc2c5627-14dd-4d04-907c-c5023bf9ec37)





