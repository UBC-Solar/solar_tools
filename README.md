# Welcome to the UBC Solar tools / tests repo!

This repository is a place to store testing scripts / tools that have a general purpose use case as well as raw data from tests we conduct using these tools.

For example, our SCPI scripts that are used to interface with our DMM's and function generators can be used for any iteration of the car. These scripts should live in this repo.

Testing data and associates visualization scripts should also be stored here. For example, see the control_board_current_characterization branch where we store raw CSV files from the oscilloscope and associated Matplotlib Python scripts.

### How to use
Create a new branch in the repo.

The naming scheme for branches is the same as used in the [firmware repo](https://github.com/UBC-Solar/firmware_v4):  
`user/<name>/<project>/<feature>`

On the new branch, create a new folder in /projects. Do all development inside this folder.
