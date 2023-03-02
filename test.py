from nyct_gtfs import NYCTFeed
from dotenv import load_dotenv
import os

load_dotenv()
feed = NYCTFeed("Q", api_key=os.getenv("MTA_KEY"))
trains = feed.trips
print(trains)
