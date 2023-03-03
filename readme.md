### Kyle's RGB LED Matrix in Python

Prerequisites:
 - Follow the guide [here](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/bindings/python/README.md) to
   build the python bindings for rpi-rgb-led-matrix
 - Create a `.env` file containing your [mta gtfs](https://new.mta.info/developers) API key as `MTA_KEY={key}`
 - run `sudo pip install -r requirements.txt`
 - add `sudo /path/to/trains.py` to your crontab to start it up on boot/schedule
