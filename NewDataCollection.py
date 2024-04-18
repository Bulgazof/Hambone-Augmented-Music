import pygame as py
import serial
import json
import keyboard

ser = serial.Serial('COM6', 9600)
py.init()

# Enter number for new json file
file_number = input("Enter a label for the JSON file: ")

user_input = input()


data = []
label = None
thresh = None
coordinates = []

while True:

    input_data = str(ser.readline(), encoding='utf-8').replace(" ", "")
    ser.reset_input_buffer()
    shortened_data = input_data[:-2]
    # turns string into list
    # struct of processed_data = [label,thresh,aX,aY,aZ,rX,rY,rZ]
    processed_data = shortened_data.split(",")
    thresh = processed_data[1]
    coordinates = processed_data[2:]

    # Pauses code and relabels the label to the input value
    if thresh != 0:
        label = keyboard.read_key()
        print(label)
    else:
        label = 0

    # will only run once window is closed
    if user_input.lower() == 'q':
        filename = f"Training set {file_number}.json"

        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
        exit()               

    coordinates = []

    data.append({
        "label": label,
        "thresh": thresh,
        "coordinates": coordinates,
    })


    # Limit the framerate to 60FPS







