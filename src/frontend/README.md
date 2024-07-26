# Hyperledger AIFAQ

## Getting Started

First, run the development server:

```bash
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.


 ## Docker Installation Guide

 This guide provides instructions for setting up and running a Next.js application using Docker. There are two Docker configurations provided: one for development (Dockerfile.dev) and one for production (Dockerfile).

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose (optional but recommended)

**Production Setup**

To set up and run the Next.js application in a production environment, follow these steps:

1. Build the Docker Image

Run the following command to build the Docker image for production:
```
docker build -t aifaq-next:prod .
```
2.  Run the Docker Container
Run the following command to start the Docker container in production mode:

```
docker run -p 3000:3000 --rm aifaq-next:prod
```
You should now be able to access your Next.js application in production mode at http://localhost:3000.
