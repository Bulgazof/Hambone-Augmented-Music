# Below is the main code for actually running the system.  Due to the implementation of bluetooth the code
# has become quite the jumble of oddly placed functions and such, as apparently the loop only runs within
# the notification handler created by the Bleak Client

import asyncio
import numpy as np
from bleak import BleakClient
import tensorflow as tf
import rtmidi
import threading
from playsound import playsound
import time

address = "74E36741-E152-90CD-4C31-6CD184A832D2"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
CHARACTERISTIC_UUID = (
    "beb5483e-36e1-4688-b7f5-ea07361b26a8"
)

model = tf.keras.models.load_model("cnn_model.keras")

# Various stuff for controlling the sound of the system
velocity = 100
drum = 0
drum_version = '2'
note_on = [0x90, drum, velocity]
note_off = [0x80, drum, velocity]

def play_sound_async(file_path):
    threading.Thread(target=playsound, args=(file_path,), daemon=True).start()

def sound_controller(prediction):
    """
    Pass in the predicted value and converts it into a drum sound
    """
    local_drum = 0
    # Tom 1
    if drum_version == '1':
        if prediction == '1':  # check what data type is being sent\
            play_sound_async('SoundController/1. mid-tom.wav')

        # Tom 2
        elif prediction == '2':
            play_sound_async('SoundController/2. floor-tom.wav')

        # Crash
        elif prediction == '3':
            play_sound_async('SoundController/3. Crash.wav')

        # High hat
        elif prediction == '4':
            play_sound_async('SoundController/4. HiHat.wav')

    elif drum_version == '2':
        if prediction == '1':  # check what data type is being sent
            play_sound_async('SoundController/5. low-bongo.wav')

        # Tom 2
        elif prediction == '2':
            play_sound_async('SoundController/6. split bongo.wav')

        # Crash
        elif prediction == '3':
            play_sound_async('SoundController/7. kalimba.wav')

        # High hat
        elif prediction == '4':
            play_sound_async('SoundController/8. Marimba.wav')

    elif drum_version == '3':
        if prediction == '1':  # check what data type is being sent
            play_sound_async('SoundController/9. HandPan1.wav')

        # Tom 2
        elif prediction == '2':
            play_sound_async('SoundController/10. HandPan 2.wav')

        # Crash
        elif prediction == '3':
            play_sound_async('SoundController/11. HandPan 3.wav')

        # High hat
        elif prediction == '4':
            play_sound_async('SoundController/12. HandPan 4.wav')


def process_data(data_string):
    """
    Used to convert the incoming bluetooth transmissions into lists
    """
    decoded_data = data_string.decode("utf-8")
    processed_data = [int(x) for x in decoded_data.split(",") if x.strip()]
    return processed_data

int_temp = 0
np_storage = []
def notification_handler(sender, data):
    """
    This block is where the code is actually being run in the bluetooth loop
    """
    x = process_data(data)
    if len(np_storage) < 50:
        np_storage.append(x)
    else:
        # print(model.predict())
        drumdrum = str(np.argmax(model.predict(np.array(np_storage).reshape(1,50,7))))
        if drumdrum == '1' or drumdrum == '2' or drumdrum == '3' or drumdrum == '4':
            sound_controller(drumdrum)
        np_storage.clear()




async def run(address):
    try:
        async with BleakClient(address, timeout=10.0) as client:
            model_number = await client.read_gatt_char(MODEL_NBR_UUID)
            print("...")
            print(model_number)
            notification_count = 0
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
            await asyncio.Future()  # Wait for a notification
    except:
        pass



loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))