# 📲🔳🏷️Automated Call System 
### Starting the Proxy Service

Run the proxy service using the dedicated compose file:

```bash
docker compose -f ./Códigos/proxy/docker-compose.proxy.yml up -d
```

This will start the Nginx container on port `80` and connect to the existing `qr_network`.

### Configuration Files

- **`Códigos/proxy/nginx.conf`** — Main Nginx configuration
  - Routes `/` to the frontend service
  - Routes `/api/` to the backend service
  - Serves static files from `/static/`

- **`Códigos/proxy/docker-compose.proxy.yml`** — Compose configuration for the proxy service
  - Mounts `nginx.conf` in read-only mode
  - Mounts frontend static files (requires `collectstatic` to be run on frontend)
  - Depends on `frontend` and `backend` services

### Volumes

The proxy mounts:
- `./Códigos/proxy/nginx.conf` → `/etc/nginx/nginx.conf` (read-only)
- `./Códigos/frontend/static` → `/var/www/static` (read-only)

Ensure the frontend runs `collectstatic` to populate the static files directory.

### Accessing the Application

- **Frontend**: `http://localhost/`
- **Backend API**: `http://localhost/api/`
- **Static Files**: `http://localhost/static/`

### Stopping the Proxy

```bash
docker compose -f ./Códigos/proxy/docker-compose.proxy.yml down
```

### Logs

View proxy logs:

```bash
docker compose -f ./Códigos/proxy/docker-compose.proxy.yml logs -f proxy
```

---
