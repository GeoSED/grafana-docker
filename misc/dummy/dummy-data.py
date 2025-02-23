import influxdb_client, os, time, random
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Environment variables for InfluxDB token and organization
token = os.environ.get("INFLUXDB_TOKEN")
org = "GeoSED"
url = "http://47.129.43.77:8086"

# Create InfluxDB client
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Specify the bucket names
bucket_water_level = "GeoSEDWaterLevel"
bucket_water_flow_rate = "GeoSEDWaterFlowRate"
bucket_river_discharge = "GeoSEDRiverDischarge"
bucket_cpu_speed = "GeoSEDCPUSpeed"
bucket_cpu_temp = "GeoSEDCPUTemperature"
bucket_cpu_usage = "GeoSEDCPUUsage"
bucket_temp = "GeoSEDTemperature"
bucket_humidity = "GeoSEDHumidity"

# Create the write API
write_api = write_client.write_api(write_options=SYNCHRONOUS)

def get_river_discharge(water_level, water_flow):
    width = 103.3550  # Width of the river in meters
    if water_level is not None and water_flow is not None:
        river_x_section_area = width * water_level  # Cross-sectional area of the river
        river_discharge = river_x_section_area * water_flow  # Calculate discharge
        return round(river_discharge, 2)  # Round to 2 decimal places
    return None

# Write data every 5 seconds
while True:
    # Generate random values
    water_level_value = round(random.uniform(0.8, 1.1), 2)  # Water level: 0.8 to 1.1
    water_flow_rate_value = round(random.uniform(1.8, 2.0), 2)  # Water flow rate: 1.8 to 2.0
    cpu_temp = round(random.uniform(40.0, 60.0), 2)
    cpu_speed = round(random.uniform(600, 1800), 2)
    cpu_usage = round(random.uniform(10.0, 90.0), 2)
    dht_temp = round(random.uniform(20.0, 35.0), 2)
    dht_hum = round(random.uniform(30.0, 70.0), 2)

    # Calculate river discharge
    river_discharge_value = get_river_discharge(water_level_value, water_flow_rate_value)

    # Create points
    point_water_level = Point("water-level").tag("device", "lidar-lite").tag("location", "cdo-pelaez").field("water_level", water_level_value)
    point_water_flow_rate = Point("water-flow-rate").tag("device", "camera").tag("location", "cdo-pelaez").field("flow_rate", water_flow_rate_value)
    point_river_discharge = Point("river-discharge").tag("device", "camera").tag("location", "cdo-pelaez").field("discharge", river_discharge_value)
    point_cpu_temp = Point("cpu-temperature").tag("device", "raspberry-pi").tag("location", "cdo-pelaez").field("cpu_temp", cpu_temp)
    point_cpu_speed = Point("cpu-speed").tag("device", "raspberry-pi").tag("location", "cdo-pelaez").field("cpu_speed", cpu_speed)
    point_cpu_usage = Point("cpu-usage").tag("device", "raspberry-pi").tag("location", "cdo-pelaez").field("cpu_usage", cpu_usage)
    point_temp = Point("temperature").tag("device", "dht22").tag("location", "cdo-pelaez").field("temperature", dht_temp)
    point_humidity = Point("humidity").tag("device", "dht22").tag("location", "cdo-pelaez").field("humidity", dht_hum)

    # Write points to their respective buckets
    write_api.write(bucket=bucket_water_level, org=org, record=point_water_level)
    write_api.write(bucket=bucket_water_flow_rate, org=org, record=point_water_flow_rate)
    write_api.write(bucket=bucket_river_discharge, org=org, record=point_river_discharge)
    write_api.write(bucket=bucket_cpu_temp, org=org, record=point_cpu_temp)
    write_api.write(bucket=bucket_cpu_speed, org=org, record=point_cpu_speed)
    write_api.write(bucket=bucket_cpu_usage, org=org, record=point_cpu_usage)
    write_api.write(bucket=bucket_temp, org=org, record=point_temp)
    write_api.write(bucket=bucket_humidity, org=org, record=point_humidity)

    # Print for debugging (optional)
    print(f"Written water level: {water_level_value}, water flow rate: {water_flow_rate_value}, river discharge: {river_discharge_value}")
    print(f"CPU Temp: {cpu_temp}, CPU Speed: {cpu_speed} MHz, CPU Usage: {cpu_usage}%")
    print(f"DHT Temp: {dht_temp}, DHT Humidity: {dht_hum}")

    # Sleep for 5 seconds before writing the next points
    time.sleep(5)
