from nyct_gtfs import NYCTFeed
from dotenv import load_dotenv
import os

load_dotenv()
async def train_estimates(line: str, stop_id: str):
    feed = NYCTFeed(line, api_key=os.getenv("MTA_KEY"), fetch_immediately=False)
    await feed.refresh_async()
    trips = feed.filter_trips(headed_for_stop_id=stop_id)
    stop_time_updates = [trip.stop_time_updates for trip in trips]
    times = [[update.arrival for update in update_list if update.stop_id == stop_id] for update_list in stop_time_updates]
    times = [time_list[0] for time_list in times]
    return times

