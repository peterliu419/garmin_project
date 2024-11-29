# garmin_project
project_root/
│
├── src/
│   ├── producer/
│   │   ├── __init__.py
│   │   ├── producer_app.py
│   │   └── producer_client.py
│   │
│   ├── consumer/
│   │   ├── __init__.py
│   │   ├── consumer_app.py
│   │   └── consumer_client.py
│   │
│   └── utils/
│       └── redis_controller.py
│
├── docker/
│   ├── Dockerfile.producer-app
│   ├── Dockerfile.producer-client
│   ├── Dockerfile.consumer-app
│   └── Dockerfile.consumer-client
│
├── docker-compose.yml
├── prometheus.yml
├── requirements.txt
├── build_docker_images.sh
├── .gitignore
├── README.md
└── Architecture.png