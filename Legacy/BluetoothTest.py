import asyncio
import numpy as np
from bleak import BleakClient
import tensorflow as tf

address = "74E36741-E152-90CD-4C31-6CD184A832D2"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
CHARACTERISTIC_UUID = (
    "beb5483e-36e1-4688-b7f5-ea07361b26a8"
)

model = tf.keras.models.load_model("cnn_model.keras")

def process_data(data_string):
  # Decode the data assuming it's UTF-8 encoded bytes
  decoded_data = data_string.decode("utf-8")

  # Use a list comprehension to convert strings to integers and remove extra characters (if needed)
  processed_data = [int(x) for x in decoded_data.split(",") if x.strip()]

  # Return the processed list
  return processed_data

int_temp = 0
np_storage = []



def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    x = process_data(data)
    if len(np_storage) < 50:
        np_storage.append(x)
    else:
        # print(model.predict())
        print(np.argmax(model.predict(np.array(np_storage).reshape(1,50,7))))
        np_storage.clear()


async def run(address):
    try:
        async with BleakClient(address, timeout=10.0) as client:
            model_number = await client.read_gatt_char(MODEL_NBR_UUID)
            print("...")
            print(model_number)
            notification_count = 0
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
            while True:
                await asyncio.Future()  # Wait for a notification
                notification_count += 1
                print("Bababooey")
                if notification_count >= 10:
                    print(np_storage)
                    notification_count = 0  # Reset counter
                    np_storage.clear()  # Clear storage (optional)
    except:
        pass



loop = asyncio.get_event_loop()

loop.run_until_complete(run(address))