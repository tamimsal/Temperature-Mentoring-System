import mysql.connector
import pika
import json

db_config = {
    'user': 'tamim',
    'password': '22585933',
    'host': 'localhost',
    'database': 'switch_db'
}

rabbitmq_host = 'localhost'
task_queue = 'task_queue'

def get_switches():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM switches")
    switches = cursor.fetchall()
    conn.close()
    return switches

def publish_tasks(switches):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=task_queue)
    
    for switch in switches:
        message = json.dumps(switch)
        channel.basic_publish(exchange='', routing_key=task_queue, body=message)
        print(f"Published task for switch: {switch['switch_name']}")

    connection.close()

if __name__ == "__main__":
    switches = get_switches()
    publish_tasks(switches)
