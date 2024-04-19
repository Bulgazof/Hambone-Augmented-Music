# Hambone-Augmented-Music
HAM

> The Hamboner V1 is a project created by Daniel Pfeiffer and Christopher Nase for CreaTe M7.  A hodgepodge of testing and various other forms of code, it encompasses the radical development techniques that are used when both rapid prototyping and time pressure are placed on two hard working yet slightly novice students!

## Hardware Overview
Below is a diagram of the overall layout of the devices used for the project.  The GY-521 is connected to the tiny ML with an I2C cable.  The PSU is a buckboost converter connected to the main board with 3.3V out.
<img width="968" alt="Screenshot 2024-04-18 at 22 24 44" src="https://github.com/Bulgazof/Hambone-Augmented-Music/assets/139565723/f707f139-a7c3-418a-be48-a2e37cc65758">

## Software Overview
The organization of the files goes as follows

* Folder - CompletedTrainingCode (Software collecting data on ESP)
* Folder - Data_Processing (Code for processing the raw data for use in training either the CNN or LSTM model)
  *   Folder - Raw_csvs (Used for data processing)
  *   Folder - Temp (Just temp stuff, feel free to ignore)
  *   Folder - Training sets (the actual raw JSON files collected from training sessions)
  *   File - DataProcessing_CNN.py (Turns Training set stuff into usable frame json)
  *   File - DataProcessing_LSTM.py (Turns Training set stuff into usable frame csv)
  *   File - NewDataCollection.py (Used to collect the raw data with labels)
* Folder - Legacy (Bunch of misc testing stuff)
* Folder - SoundController (Sound Samples)
  *   File - SoundController.py (Testing for keyboard based sound playing)
* File - Hambone_CNN.py (Testing and validation for the CNN model)
* File - Hambone_LSTM.py (Testing and validation for the LSTM model)
* File - Hamboner_V1_MainCode.py (The compiled code for actually connecting to the V1 and playing sounds with it
* File - Saved_CNN.py (Testing Saved)
* File - Saved_LSTM.py (Testing Saved)
* File - Hamboner_V1_ESP32S2 (Software for the TinyML Board)

## Code Structure
<img width="1018" alt="Screenshot 2024-04-18 at 23 08 17" src="https://github.com/Bulgazof/Hambone-Augmented-Music/assets/139565723/e67c25ca-c7d5-4927-9db7-833e252f2751">
