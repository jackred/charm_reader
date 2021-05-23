# charm_reader

## Installation

### Windows

- Download the [release](https://github.com/jackred/charm_reader/releases/tag/0.2.1)
- Extract it wherever you want
- Install *Python* from the Microsoft Store
- Open a `powershell` window and move in the folder of the project
  - You can either open it from the search menu, then copy the location of the project from the address bar in a file explorer, and type `cd ADRESS`
  - You can also directly type `powershell` in the address bar at the top of the file explorer opened at your project location (you can also use the shortcuts `Alt`+`D` or `Ctrl`+`L`)
  - You can also press *File* (at the top) and choose "*Open Windows PowerShell*"
- You can check you are in the good folder by running `dir` and check that the list of files written is the same as in your file explorer
- Write the following command: `python -m pip install -r requirements.txt`
  - Known issue: impossibility to install some package due to an OSError, see https://github.com/scikit-learn/scikit-learn/issues/19306 for details on the error and https://www.howtogeek.com/266621/how-to-make-windows-10-accept-file-paths-over-260-characters/ for fixing (the first solution with regedit works, be sure to restart your computer afterward).

### Linux

- Download the [release](https://github.com/jackred/charm_reader/releases/tag/0.2,1)
- Extract it wherever you want and open the location in a terminal
- Run `pip install -r requirements.txt` 
  - You can create a virtualenv beforehand if you don't want to install the packages globally
    - `pip install virtualenv`
    - `python -m virtualenv env`
    - `source env/bin/activate`
    - run the install command now
    - To exit the virtualenv: `deactivate`

## Running

- Make a recording:
  - The clip need to feature only the moment when you take your charm (when you press A) from the first to the last. The easiest way to do so is to look at all your charm beforehand, then come back to the first one and keep pressing A until you get the last one, then press capture.  
  - You can then trim the clip from the switch.
  - A small trick is pressing "home" before doing the recording (once you're back on the first charm) and come back, press A until the last charm and then press capture. Doing so will only record the 50 charms without the need to trim the part when you look at the charm.
- Get the recording from your switch 
  - you can use an usb-c - usb cable, connect it to your computer, and go in "Settings" > "Data Management" > "Manage Screenshots and Videos" > "Copy to PC via USB Connection"
  - you can also, very tediously, send the video one by one to your phone by using "Send to smart device"
  - You can use a third-party software (like obs) with an acquisition card and record your opening on your computer directly.
- Create a *videos* folder in the project
- Put all the recording you want in the *videos* folder
  - They will be treated in alphabetic order. By defaults, switch recording name are ordered by date, so if you use the default name, the output should be in the same order as you made the opening
  - If you use other name than the correct one, rename the videos (or do it one by one)
- Run:
  - If you are on Windows, open a `powershell` at the project location, and write `python main.py`
  - If you are on LInux, open a terminal at the project location and write `python main.py`
- Wait for the programme to finish. A file named *output.csv* should have been generated in the *videos* folder
- Be sure to clean the *videos* folder after each use, otherwise the videos will be read each time

## Detail
This tool compare a part of the frame with skill's screenshots save before, using a simple Euclidian distance between each pixel, and checking the sum of all distance against a threshold. 
### Future improvement
 - Use OCR (tesseract) to automatically recognize the character/skills (scalable for other language)
 - Use the charm cursor position to recognize which charm is being read (using the orange color)

## Issue

If you encounter any issue, please contact me on Discord (Jackred#0431) on the TCT server (https://discord.gg/twNX37b), on Twitter (@MH_JackRed) or create an issue directly on Github. 
