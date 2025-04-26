# Faust Stream Processor

This component transforms the raw station data from Kafka Connect into a more usable format.

## Overview

The Faust Stream Processor:
1. Consumes data from the Kafka Connect topic `org.chicago.cta.stations`
2. Transforms the data by extracting only the necessary fields
3. Determines the line color based on the boolean flags (red, blue, green)
4. Produces the transformed data to the topic `org.chicago.cta.stations.table.v1`

## Running the Processor

To run the Faust Stream Processor, use the following command from the `consumers` directory:

```bash
faust -A faust_stream worker -l info
```

This will start the Faust worker which will process the data from the input topic and produce it to the output topic.

## Testing

You can test the Faust Stream Processor configuration without actually processing data by running:

```bash
python test_faust_stream.py
```

This will verify that the Faust app, topics, and table are configured correctly.

## Monitoring

You can monitor the Faust Stream Processor using the Faust web UI, which is available at:

```
http://localhost:6066
```

## Troubleshooting

If you encounter issues with the Faust Stream Processor, check the following:

1. Make sure Kafka is running and accessible
2. Verify that the Kafka Connect connector is properly configured and running
3. Check that the input topic `org.chicago.cta.stations` exists and has data
4. Ensure that the output topic `org.chicago.cta.stations.table.v1` is properly configured

## Environment Variables

The Faust Stream Processor supports the following environment variables:

- `KAFKA_BROKER_URL`: The URL for the Kafka broker (default: `kafka://localhost:9092`)
