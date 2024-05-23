import pika
import json
from influxdb_client import InfluxDBClient, Point, WriteOptions

# RabbitMQ configuration
rabbitmq_host = 'localhost'
task_queue = 'task_queue'

# InfluxDB configuration
influxdb_url = "http://localhost:8086"
influxdb_token = "U8MrskFYSYFTIv1P2E9DxVD3BKh0yyMVSiwzRDNHQDikUKvUojo-iDDYkV4Lj4fD8na-uC82t_rM3JeoFIhqIA=="
influxdb_org = "ppu"
influxdb_bucket = "project1"

def get_temperature(ip_address):
    print(f"Retrieving temperature for IP: {ip_address}")
    return 25.0 + (hash(ip_address) % 10)

def write_to_influxdb(switch_name, temperature):
    print(f"Writing to InfluxDB: switch_name={switch_name}, temperature={temperature}")
    client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
    write_api = client.write_api(write_options=WriteOptions(batch_size=1))
    
    point = Point("switch_temperature") \
        .tag("switch", switch_name) \
        .field("temperature", temperature)
    
    write_api.write(bucket=influxdb_bucket, record=point)
    client.close()

def callback(ch, method, properties, body):
    switch = json.loads(body)
    ip_address = switch['ip_address']
    switch_name = switch['switch_name']
    temperature = get_temperature(ip_address)
    print(f"Switch: {switch_name}, IP: {ip_address}, Temperature: {temperature}")
    write_to_influxdb(switch_name, temperature)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_tasks():
    print("Starting to consume tasks from RabbitMQ...")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=task_queue)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=task_queue, on_message_callback=callback)
    
    for method_frame, properties, body in channel.consume(task_queue):
        print("Received message from RabbitMQ")
        callback(channel, method_frame, properties, body)
    
    channel.start_consuming()

if __name__ == "__main__":
    consume_tasks()
