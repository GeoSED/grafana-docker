import influxdb_client, os, time, random
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Environment variables for InfluxDB token and organization
token = os.environ.get("INFLUXDB_TOKEN")
org = "GeoSED"
url = "http://localhost:8086"

# Create InfluxDB client
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Specify the bucket names
bucket_water_level = "GeoSEDWaterLevel"
bucket_water_flow_rate = "GeoSEDWaterFlowRate"
bucket_river_discharge = "GeoSEDRiverDischarge"

# Create the write API
write_api = write_client.write_api(write_options=SYNCHRONOUS)

def get_river_discharge(water_level, water_flow):
    width = 103.3550  # Width of the river in meters
    if water_level is not None and water_flow is not None:
        river_x_section_area = width * water_level  # Cross-sectional area of the river
        river_discharge = river_x_section_area * water_flow  # Calculate discharge
        return round(river_discharge, 2)  # Round to 2 decimal places
    return None

# Write data every 10 seconds
while True:
    # Generate random values
    water_level_value = round(random.uniform(0.8, 1.1), 2)  # Water level: 0.8 to 1.1
    water_flow_rate_value = round(random.uniform(1.8, 2.0), 2)  # Water flow rate: 1.8 to 2.0

    # Calculate river discharge
    river_discharge_value = get_river_discharge(water_level_value, water_flow_rate_value)

    # Create points for water level, water flow rate, and river discharge
    point_water_level = (
        Point("water-level")
        .tag("location", "cdo-pelaez")
        .field("water_level", water_level_value)
    )

    point_water_flow_rate = (
        Point("water-flow-rate")
        .tag("location", "cdo-pelaez")
        .field("flow_rate", water_flow_rate_value)
    )

    point_river_discharge = (
        Point("river-discharge")
        .tag("location", "cdo-pelaez")
        .field("discharge", river_discharge_value)
    )

    # Write points to their respective buckets
    write_api.write(bucket=bucket_water_level, org=org, record=point_water_level)
    write_api.write(bucket=bucket_water_flow_rate, org=org, record=point_water_flow_rate)
    write_api.write(bucket=bucket_river_discharge, org=org, record=point_river_discharge)

    # Print for debugging (optional)
    print(f"Written water level: {water_level_value}, water flow rate: {water_flow_rate_value}, river discharge: {river_discharge_value}")

    # Sleep for 10 seconds before writing the next points
    time.sleep(10)
