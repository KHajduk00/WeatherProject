import threading
from collector import collect_data_for_all_cities, COLLECTION_INTERVAL
import time
import logging

logger = logging.getLogger(__name__)

class CollectorService:
    def __init__(self):
        self.running = False
        self.thread = None
        self.last_collection_time = None
        self.collection_interval = COLLECTION_INTERVAL

    def start_collection(self):
        if self.running:
            return False, "Collector is already running"
        
        self.running = True
        self.thread = threading.Thread(target=self._collection_loop)
        self.thread.daemon = True
        self.thread.start()
        return True, "Collector started successfully"

    def stop_collection(self):
        if not self.running:
            return False, "Collector is not running"
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=10)
        return True, "Collector stopped successfully"

    def _collection_loop(self):
        while self.running:
            try:
                collect_data_for_all_cities()
                self.last_collection_time = time.time()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error in collection loop: {e}")
                time.sleep(10)  # Wait before retrying

    def get_status(self):
        return {
            "running": self.running,
            "last_collection": self.last_collection_time,
            "collection_interval": self.collection_interval
        }

    def set_interval(self, interval):
        if interval < 60:  # Minimum 1 minute
            return False, "Interval must be at least 60 seconds"
        self.collection_interval = interval
        return True, f"Collection interval set to {interval} seconds"