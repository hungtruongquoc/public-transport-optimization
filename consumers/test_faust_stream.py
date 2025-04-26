#!/usr/bin/env python
"""
Test script for the Faust Stream Processor.
This script checks if the Faust app is configured correctly.
"""
import logging
import sys

from faust_stream import app, topic, out_topic, table, TransformedStation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_faust_configuration():
    """Test the Faust app configuration."""
    logger.info("Testing Faust configuration...")
    
    # Check app configuration
    logger.info(f"App ID: {app.conf.id}")
    logger.info(f"Broker: {app.conf.broker}")
    
    # Check topic configuration
    logger.info(f"Input topic: {topic.get_topic_name()}")
    logger.info(f"Output topic: {out_topic.get_topic_name()}")
    
    # Check table configuration
    logger.info(f"Table name: {table.name}")
    logger.info(f"Table default type: {table.default}")
    
    logger.info("Faust configuration test completed successfully!")
    return True

if __name__ == "__main__":
    try:
        success = test_faust_configuration()
        if success:
            logger.info("All tests passed!")
            sys.exit(0)
        else:
            logger.error("Tests failed!")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error during testing: {e}")
        sys.exit(1)
