from nyct_gtfs import NYCTFeed
from dotenv import load_dotenv
import os

load_dotenv()
class TrainTimes:

    def __init__(self, line: str, stop_id: str):
        self.stop_id = stop_id
        self.feed = NYCTFeed(line, api_key=os.getenv("MTA_KEY"), fetch_immediately=False)

    async def refresh(self):
        try:
            await self.feed.refresh_async()
            trips = self.feed.filter_trips(headed_for_stop_id=self.stop_id)
            stop_time_updates = [trip.stop_time_updates for trip in trips]
            times = [[update.arrival for update in update_list if update.stop_id == self.stop_id] for update_list in stop_time_updates]
            self.times = sorted([time_list[0] for time_list in times])
        except Exception as e:
            print(f"failed to get train times: {e}")
        
    def get_times(self):
        return self.times



