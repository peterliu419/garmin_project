## Project Structure

```txt
project_root/
│
├── src/                     # Source code directory
│   ├── producer/            # Producer service: generates and sends user activity data
│   │   ├── __init__.py      # Package initialization
│   │   ├── producer_app.py  # Flask API to produce and push data to Redis
│   │   └── producer_client.py # CLI or script to simulate producer behavior
│   │
│   └── consumer/            # Consumer service: processes and aggregates data
│       ├── __init__.py      # Package initialization
│       ├── consumer_app.py  # Flask API to consume and aggregate data from Redis
│       └── consumer_client.py # CLI or script to simulate consumer behavior
│
├── docker/                  # Docker setup for the project
│   ├── Dockerfile.producer-app  # Dockerfile for the producer API
│   ├── Dockerfile.producer-client # Dockerfile for the producer CLI
│   ├── Dockerfile.consumer-app  # Dockerfile for the consumer API
│   └── Dockerfile.consumer-client # Dockerfile for the consumer CLI
│
├── docker-compose.yml       # Orchestration file for multi-container setup
├── prometheus.yml           # Configuration file for Prometheus monitoring
├── requirements.txt         # Python dependencies
├── build_docker_images.sh   # Script to build Docker images
├── .gitignore               # Ignored files for version control
├── README.md                # Project documentation
└── Architecture.png         # High-level architecture diagram