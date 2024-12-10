# Smart Watch Activity Log Monitoring System

A monitoring system for Smart Watch user activity logs using Redis Cluster, implemented with Flask applications and monitored through Prometheus & Grafana.

## Overview

This project simulates a system that:

- Tracks user activity logs from smart watches (Producer)
- Stores logs in Redis Cluster
- Allows internal users to extract logs for reporting purposes (Consumer)
- Simulate random delay and failure

## Architecture

The system consists of three main components:
![Project Structure Diagram](project_structure.jpeg)

### Core Services

- Producer: Generates and processes simulated user activity data
- Consumer: Handles data consumption for internal users
- Redis Cluster: 3-node setup for distributed data storage

### Monitoring Stack

- Redis-exporter: Exports Redis metrics
- Prometheus: Collects and monitors service metrics
- Grafana: Visualizes collected metrics

## Deployment

The project uses Docker Compose for local deployment, with:

- Pre-built images hosted on GitHub Container Registry on this repository
- Official images from Docker Hub for Redis, Redis Exporter, Prometheus, and Grafana

## Project Root
```txt
project_root/
├── docker/                        # Docker setup for the project
│   ├── Dockerfile.producer-app    # Dockerfile for the producer API
│   ├── Dockerfile.producer-client # Dockerfile for the producer CLI
│   ├── Dockerfile.consumer-app    # Dockerfile for the consumer API
│   └── Dockerfile.consumer-client # Dockerfile for the consumer CLI
│
├── src/                           # Source code directory
│   ├── producer/                  # Producer service: generates and sends user activity data
│   │   ├── __init__.py            # Package initialization
│   │   ├── producer_app.py        # Flask API to produce and push data to Redis
│   │   └── producer_client.py     # CLI or script to simulate producer behavior
│   │
│   └── consumer/                  # Consumer service: processes and aggregates data
│       ├── __init__.py            # Package initialization
│       ├── consumer_app.py        # Flask API to consume and aggregate data from Redis
│       └── consumer_client.py     # CLI or script to simulate consumer behavior
│
├── docker-compose.yml             # Orchestration file for multi-container setup
├── prometheus.yml                 # Configuration file for Prometheus monitoring
├── requirements.txt               # Python dependencies for Dockerfile configuration
├── build_docker_images.sh         # Script to build Docker images
├── project_structure.jpeg         # Diagram of project structure
├── init-cluster.sh                # Script to initialize Redis cluster
├── .gitignore                     # Ignored files for version control
└── README.md                      # Project documentation
```

### Quick Start

1. Initialize and run services:

```bash
docker-compose up --build
```

2. Access monitoring dashboards:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
3. Stop services:

```bash
docker-compose down -v
```