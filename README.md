# Switch Temperature Monitoring System
This project is designed to monitor the temperature of network switches using a distributed architecture with Crontab, RabbitMQ, MariaDB, and InfluxDB. The system periodically collects temperature data from switches and stores it in a time-series database for analysis.

# Features
Scheduled Data Collection: A Crontab job triggers the coordinator script every five minutes to start the data collection process.
Task Queue Management: RabbitMQ is used to manage and distribute data collection tasks to multiple collectors.
Relational Database: MariaDB stores the list of switches, which the coordinator retrieves and distributes tasks for.
Time-Series Database: InfluxDB is used to store the collected temperature data.

# Architecture
Sender: Triggered by Crontab, retrieves a list of switches from MariaDB and writes collection tasks to RabbitMQ.
Receiver: Consumes tasks from RabbitMQ, retrieves temperature data from switches, and writes the data to InfluxDB.

#Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.
