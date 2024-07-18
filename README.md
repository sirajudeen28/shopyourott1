# shopyourott1

## Steps to run
#### * Create Virtual environment
#### * pip install virtualenv 
#### * virtualenv venv
#### * Activate the virtualenv
#### * pip install -r requirements.txt
#### * Make sure to mention the video file path in the main.py and input, output folder paths in the distinct_outfit.py
#### * python main.py

### This script takes a video file as input and extracts the frames where pixels have changed over a threshold from previous frame.
### Then it calls another script(distinct_outfit.py) from inside the code to get the distinct images out of the extracted image frames.
### Lens API code to be added to check similar products.