# University Portal - Running Both Services

## Quick Start

```bash
cd /workspace/university-portal

# Terminal 1 - Start Backend
cd apps/api && python3 manage.py runserver 8001

# Terminal 2 - Start Frontend  
cd apps/web && npm run dev
```

## Or use the startup script:

```bash
./start.sh
```

## Access Points

| Service | URL | Status |
|---------|-----|-------|
| **Frontend** | http://localhost:3000 | ✅ |
| **Backend API** | http://localhost:8001 | ✅ |
| **API Docs** | http://localhost:8001/docs | ✅ |

## Test APIs

```bash
# Get config
curl http://localhost:8001/api/config

# Login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@uni.edu","password":"admin123"}'

# Countries (234)
curl http://localhost:8001/api/auth/nigeria/countries
```

## Login Credentials

- **Email:** admin@uni.edu
- **Password:** admin123
