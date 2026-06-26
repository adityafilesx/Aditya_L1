# 15. Deployment Guide

This document describes how to deploy the Aditya-L1 Space Weather Intelligence Platform to staging or production infrastructure.

---

## 🐋 Containerized Deployment (Docker)

A standard multi-container configuration is defined to isolate components:

### 1. Backend Dockerfile (`backend/Dockerfile` representation)
```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Frontend Dockerfile (`frontend/Dockerfile` representation)
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## ⚙️ Environment Variables

### 1. Backend Environment Configurations
Create a `backend/.env` file in the production environment:
```env
PORT=8000
HOST=0.0.0.0
MODEL_PATH=/app/data/models/ensemble_forecaster.pkl
WANDB_API_KEY=your_key_here  # For training monitoring
```

### 2. Frontend Environment Configurations
Create a `frontend/.env` file:
```env
VITE_API_URL=https://api.solar-control.isro.gov.in
VITE_WS_URL=wss://api.solar-control.isro.gov.in/ws/live
```

---

## 🔀 Nginx Reverse Proxy Setup

To route traffic securely and handle WebSocket upgrading, deploy Nginx:

```nginx
server {
    listen 443 ssl;
    server_name solar-control.isro.gov.in;

    # Static Frontend
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # API REST requests
    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket connection
    location /ws/ {
        proxy_pass http://backend:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
```
*   *Note: Ensure to use `wss://` on the client side when proxying SSL connections.*
