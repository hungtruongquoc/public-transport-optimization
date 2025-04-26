"""Defines trends calculations for stations"""
import logging
import os

import faust


logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


# TODO: Define a Faust Stream that ingests data from the Kafka Connect stations topic and
#   places it into a new topic with only the necessary information.
app = faust.App(
    "stations-stream",
    broker=os.getenv("KAFKA_BROKER_URL", "kafka://localhost:9092"),
    store="memory://"
)
# Define the input Kafka Topic from Kafka Connect
topic = app.topic("org.chicago.cta.stations", value_type=Station)
# Define the output Kafka Topic
out_topic = app.topic("org.chicago.cta.stations.table.v1", partitions=1)
# Define a Faust Table
table = app.Table(
    "stations_table",
    default=TransformedStation,
    partitions=1,
    changelog_topic=out_topic,
)


@app.agent(topic)
async def process_stations(stations):
    """
    Process station data from Kafka Connect and transform it to the required format.
    """
    async for station in stations:
        # Determine the line color based on boolean flags
        line = None
        if station.red:
            line = "red"
        elif station.blue:
            line = "blue"
        elif station.green:
            line = "green"
        else:
            logger.warning(f"No line color found for station {station.station_id}")
            line = "unknown"

        # Create a transformed station record
        transformed = TransformedStation(
            station_id=station.station_id,
            station_name=station.station_name,
            order=station.order,
            line=line
        )

        # Update the table with the transformed station
        table[station.station_id] = transformed

        # Log the transformation for debugging
        logger.info(f"Transformed station: {station.station_id} to line {line}")


if __name__ == "__main__":
    app.main()
