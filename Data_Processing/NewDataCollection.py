import pygame as py
import serial
import json
import keyboard
import time

ser = serial.Serial('COM6', 9600)
py.init()

# Enter number for new json file
print("Enter a label for the JSON file: ")
file_number = keyboard.read_key()
time.sleep(1)
print("Enter label version: ")
ver_number = keyboard.read_key()

data = []
label = None
thresh = None
coordinates = []

while True:

    # user_input = input()
    input_data = str(ser.readline(), encoding='utf-8').replace(" ", "")
    # ser.reset_input_buffer()
    # input_data = ser.readline().decode('utf-8')  # Decode and remove trailing newline
    shortened_data = input_data[:-2]
    # turns string into list
    # struct of processed_data = [label,thresh,aX,aY,aZ,rX,rY,rZ]
    processed_data = shortened_data.split(",")

    thresh = processed_data[1]
    print(thresh)
    coordinates = processed_data[2:]

    # Pauses code and relabels the label to the input value
    if thresh == str(0):
        label = 0
    else:
        print("babatoobey")
        label = keyboard.read_key()
        print(label)

    data.append({
        "label": label,
        "thresh": thresh,
        "coordinates": coordinates,
    })

    if keyboard.is_pressed('q'):
        filename = f"Training set {file_number} {ver_number}.json"

        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
        quit()


