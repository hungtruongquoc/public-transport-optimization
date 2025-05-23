"""Creates a turnstile data producer"""
import logging
from pathlib import Path

from confluent_kafka import avro

from .producer import Producer
from .turnstile_hardware import TurnstileHardware


logger = logging.getLogger(__name__)


class Turnstile(Producer):
    key_schema = avro.load(f"{Path(__file__).parents[0]}/schemas/turnstile_key.json")

    # Load the value schema for turnstile events
    value_schema = avro.load(
        f"{Path(__file__).parents[0]}/schemas/turnstile_value.json"
    )

    def __init__(self, station):
        """Create the Turnstile"""
        station_name = (
            station.name.lower()
            .replace("/", "_and_")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("'", "")
        )

        # Define the topic name following a consistent naming convention
        topic_name = f"org.chicago.cta.station.turnstile.v1"
        super().__init__(
            topic_name,
            key_schema=Turnstile.key_schema,
            value_schema=Turnstile.value_schema,
            num_partitions=1,
            num_replicas=1
        )
        self.station = station
        self.turnstile_hardware = TurnstileHardware(station)

    def run(self, timestamp, time_step):
        """Simulates riders entering through the turnstile."""
        num_entries = self.turnstile_hardware.get_entries(timestamp, time_step)

        # Emit a message to the turnstile topic for each entry
        try:
            for _ in range(num_entries):
                self.producer.produce(
                    topic=self.topic_name,
                    key={"timestamp": self.time_millis()},
                    value={
                        "station_id": self.station.station_id,
                        "station_name": self.station.name,
                        "line": self.station.color.name
                    }
                )
            logger.info(f"Emitted {num_entries} turnstile events for station {self.station.name}")
        except Exception as e:
            logger.error(f"Failed to emit turnstile event: {e}")
