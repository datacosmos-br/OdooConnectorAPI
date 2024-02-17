# OdooConnectorAPI

## Overview

OdooConnectorAPI is a RESTful API designed to facilitate communication between external applications and the Odoo ERP system. It leverages FastAPI for efficient asynchronous communication and is containerized using Docker for easy deployment. This project also includes a Helm chart for Kubernetes deployments, allowing for scalable and manageable production environments.

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Kubernetes cluster (for Helm deployment)
- Helm 3

### Local Setup

1. **Clone the repository:**

```bash
git clone https://github.com/datacosmos-br/OdooConnectorAPI.git
cd OdooConnectorAPI
```

2. **Install dependencies:**

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

Copy the `.env.example` to `.env` and adjust the variables to match your Odoo setup:

```bash
cp .env.example .env
```

Edit `.env` to include your Odoo credentials and connection details.

4. **Run the application:**

```bash
uvicorn app.main:app --reload
```

### Using Docker Compose

1. **Build and run the container:**

```bash
docker-compose up --build
```

This command builds the Docker image and starts the containerized application, reading the `.env` file for environment variables.

### Deploying with Helm to Kubernetes

1. **Package the Helm chart:**

Navigate to the Helm chart directory:

```bash
cd charts/odooconnectorapi
```

Package the Helm chart:

```bash
helm package .
```

2. **Deploy the chart to your Kubernetes cluster:**

Assuming you have a Kubernetes cluster set up and your `kubectl` is configured to communicate with it:

```bash
helm install odooconnectorapi odooconnectorapi-0.1.0.tgz --values values.yaml
```

Make sure to adjust `values.yaml` according to your environment and requirements.

## Configuration

The application can be configured using environment variables. See `.env.example` for a list of available variables.

## Contributing

We welcome contributions! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.