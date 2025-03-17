import threading
import time
import logging
from datetime import datetime 
from app.core.config import COLLECTION_INTERVAL
from app.services.collector import collect_data_for_all_cities

logger = logging.getLogger(__name__)

class CollectorService:
    def __init__(self):
        self.running = False
        self.thread = None
        self.last_collection_time = None
        self.collection_interval = COLLECTION_INTERVAL

    def start_collection(self):
        """Start the data collection process"""
        if self.running:
            return False, "Collector is already running"
        
        self.running = True
        self.thread = threading.Thread(target=self._collection_loop)
        self.thread.daemon = True
        self.thread.start()
        logger.info("Data collection service started")
        return True, "Collector started successfully"

    def stop_collection(self):
        """Stop the data collection process"""
        if not self.running:
            return False, "Collector is not running"
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=10)
            logger.info("Data collection service stopped")
        return True, "Collector stopped successfully"

    def _collection_loop(self):
        """Main collection loop that runs in a separate thread"""
        while self.running:
            try:
                collect_data_for_all_cities()
                self.last_collection_time = time.time()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error in collection loop: {e}")
                time.sleep(10)  # Wait before retrying

    def get_status(self):
        """Get the current status of the collector service"""
        return {
            "running": self.running,
            "last_collection": self.last_collection_time,
            "collection_interval": self.collection_interval,
            "last_collection_formatted": datetime.fromtimestamp(self.last_collection_time).isoformat() if self.last_collection_time else None
        }

    def set_interval(self, interval: int):
        """Set the collection interval in seconds"""
        if interval < 60:  # Minimum 1 minute
            return False, "Interval must be at least 60 seconds"
        self.collection_interval = interval
        logger.info(f"Collection interval updated to {interval} seconds")
        return True, f"Collection interval set to {interval} seconds"