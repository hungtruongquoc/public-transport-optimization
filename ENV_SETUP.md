# Environment Variables Setup

This project now supports configuration through environment variables, which makes it more flexible for different deployment environments.

## Available Environment Variables

- `KAFKA_BROKER_URL`: The URL for the Kafka broker (default: `PLAINTEXT://localhost:9092`)
- `SCHEMA_REGISTRY_URL`: The URL for the Schema Registry (default: `http://localhost:8081`)

## How to Use

### Local Development

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your specific configuration if needed.

3. Load the environment variables before running the application:
   ```bash
   # Linux/macOS
   source .env
   
   # Windows (PowerShell)
   Get-Content .env | ForEach-Object {
       if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
           $name = $matches[1].Trim()
           $value = $matches[2].Trim()
           [Environment]::SetEnvironmentVariable($name, $value)
       }
   }
   ```

### Docker Deployment

When using Docker, you can pass environment variables in your `docker-compose.yml` file:

```yaml
services:
  producer:
    build: ./producers
    environment:
      - KAFKA_BROKER_URL=PLAINTEXT://kafka:9092
      - SCHEMA_REGISTRY_URL=http://schema-registry:8081
  
  consumer:
    build: ./consumers
    environment:
      - KAFKA_BROKER_URL=PLAINTEXT://kafka:9092
      - SCHEMA_REGISTRY_URL=http://schema-registry:8081
```

### Kubernetes Deployment

For Kubernetes deployments, you can use ConfigMaps or Secrets to manage environment variables:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kafka-config
data:
  KAFKA_BROKER_URL: "PLAINTEXT://kafka-service:9092"
  SCHEMA_REGISTRY_URL: "http://schema-registry-service:8081"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: producer-deployment
spec:
  template:
    spec:
      containers:
      - name: producer
        image: your-producer-image
        envFrom:
        - configMapRef:
            name: kafka-config
```
