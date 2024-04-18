import pygame as py
import serial
import json
import codecs

ser = serial.Serial('COM6', 9600)
py.init()


screen = py.display.set_mode(size=(300, 300))
py.display.set_caption("Ur mom")

# Initialise the py Clock for timing
# --- MIGHT NOT BE NECESSARY BASED ON CHIP FUNCTIONALITY ---
clock = py.time.Clock()

data = []
label = None
coordinates = []

while True:
    sep = False
    for event in py.event.get():

        input_data = str(ser.readline(), encoding='utf-8').replace(" ", "")
        shortened_data = input_data[:-2]
        processed_data = shortened_data.split(";")
        coordinates.append(processed_data[1:])

        print(processed_data)

        if event.type == py.QUIT:
            py.quit()

            with open('coordinates.json', 'w') as file:
                json.dump(data, file, indent=2)
            exit()

        # We will label each movement as a number
        elif event.type == py.KEYDOWN:
            print("Hello")
            if event.unicode.isdigit():
                label = event.unicode
                print(label)
                sep = True

            # We will need a function to trigger LEDs on the chip
            elif event.key == py.K_q:  # Exit the program
                break

    if label is not None and sep:
        data.append({
            "label": label,
            "sep": sep,
            "coordinates": coordinates,
        })

    for event1 in py.event.get():
        if event1.type == py.K_c:
            print(data)

    # Limit the framerate to 60FPS
    clock.tick(60)

    # py.display.flip()
