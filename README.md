# Nigerian University Portal

A comprehensive, production-ready university portal supporting:
- **British/Nigerian University System** (NUC, JAMB, TETFund aligned)
- **American University System** (Liberal arts, majors/minors)
- **Nigerian Polytechnic System** (NBTE, ND/HND)

## Quick Start

### 1. Select Your System

```bash
# For British/Nigerian University (default)
export ACADEMIC_STYLE=british_nigerian
export SYSTEM_TYPE=university

# For Nigerian Polytechnic
export ACADEMIC_STYLE=british_nigerian
export SYSTEM_TYPE=polytechnic

# For American University
export ACADEMIC_STYLE=american
export SYSTEM_TYPE=university
```

### 2. Start with Docker

```bash
# Start all services
docker-compose up -d

# Or with specific configuration
ACADEMIC_STYLE=british_nigerian SYSTEM_TYPE=university docker-compose up -d
```

### 3. Access the Application

- API: http://localhost:8001
- Web: http://localhost:3000
- Centrifugo (WebSocket): http://localhost:8000

## Configuration Presets

### Preset 1: British/Nigerian University

```json
{
  "id": "uni_british",
  "name": "British/Nigerian University",
  "system_type": "university",
  "academic_style": "british_nigerian",
  "features": {
    "grading": "A-F (70-100%)",
    "degree_duration": "4-5 years",
    "assessment": "30% CA + 70% Exam",
    "classifications": ["First Class", "Second Class Upper/Lower", "Third Class"],
    "regulators": ["NUC", "JAMB", "TETFund"]
  }
}
```

### Preset 2: Nigerian Polytechnic

```json
{
  "id": "poly_nigerian",
  "name": "Nigerian Polytechnic",
  "system_type": "polytechnic",
  "academic_style": "british_nigerian",
  "features": {
    "grading": "A-AB-B-BC-C-CD-D-E-F (Credit system)",
    "degree_duration": "2 years (ND) + 2 years (HND)",
    "assessment": "30% CA + 70% Exam",
    "classifications": ["Distinction", "Upper Credit", "Lower Credit", "Pass"],
    "regulators": ["NBTE", "JAMB"],
    "mandatory_training": "SIWES"
  }
}
```

### Preset 3: American University

```json
{
  "id": "uni_american",
  "name": "American University",
  "system_type": "university",
  "academic_style": "american",
  "features": {
    "grading": "A+ to F (4.0 scale)",
    "degree_duration": "4 years",
    "assessment": "40% CA + 60% Exam",
    "classifications": ["President's List", "Dean's List", "Good Standing"],
    "structure": "Major + Minor + General Education",
    "credits": "120 credits minimum"
  }
}
```

## API Endpoints

### Configuration API

```bash
# Get current configuration
GET /api/config

# Get all presets
GET /api/config/presets

# Set configuration
POST /api/config/set
{
  "system_type": "university",
  "academic_style": "british_nigerian",
  "university_name": "University of Nigeria"
}
```

## Project Structure

```
university-portal/
├── apps/
│   ├── api/           # Django Ninja API
│   │   ├── university/    # Core university models
│   │   ├── students/      # Student management
│   │   ├── academic/     # Courses, grades, timetable
│   │   ├── finance/      # Payments, fees
│   │   ├── admission/    # JAMB CAPS integration
│   │   ├── messaging/   # Notifications
│   │   └── users/       # Staff management
│   │
│   ├── web/            # Next.js 15 Frontend
│   ├── mobile/         # Expo Mobile App
│   └── ml-service/     # Litestar AI/ML Service
│
├── config/             # University configuration
├── packages/           # Shared packages
└── docker-compose.yml  # Docker configuration
```

## Grading Systems

### British/Nigerian (Universities)

| Grade | Score Range | Points | Description |
|-------|-------------|--------|-------------|
| A | 70-100 | 5 | Excellent |
| B | 60-69 | 4 | Very Good |
| C | 50-59 | 3 | Good |
| D | 45-49 | 2 | Pass |
| E | 40-44 | 1 | Fair Pass |
| F | 0-39 | 0 | Fail |

### Nigerian Polytechnics

| Grade | Score Range | Points | Description |
|-------|-------------|--------|-------------|
| A | 80-100 | 4.0 | Excellent |
| AB | 75-79 | 3.5 | Very Good |
| B | 70-74 | 3.25 | Very Good |
| BC | 65-69 | 3.0 | Good |
| C | 60-64 | 2.75 | Good |
| CD | 55-59 | 2.5 | Credit |
| D | 50-54 | 2.25 | Credit |
| E | 45-49 | 2.0 | Pass |
| F | 0-44 | 0.0 | Fail |

### American

| Grade | Score Range | Points |
|-------|-------------|--------|
| A+ | 97-100 | 4.0 |
| A | 93-96 | 4.0 |
| A- | 90-92 | 3.7 |
| B+ | 87-89 | 3.3 |
| B | 83-86 | 3.0 |
| B- | 80-82 | 2.7 |
| C+ | 77-79 | 2.3 |
| C | 73-76 | 2.0 |
| C- | 70-72 | 1.7 |
| D+ | 67-69 | 1.3 |
| D | 63-66 | 1.0 |
| D- | 60-62 | 0.7 |
| F | 0-59 | 0.0 |

## Degree Classifications

### British/Nigerian Universities

- **First Class**: CGPA >= 4.5
- **Second Class Upper**: CGPA >= 3.5
- **Second Class Lower**: CGPA >= 2.5
- **Third Class**: CGPA >= 2.0

### American Universities

- **President's List**: GPA >= 3.9
- **Dean's List**: GPA >= 3.5
- **Good Standing**: GPA >= 2.0

### Nigerian Polytechnics

- **Distinction**: CGPA >= 3.5
- **Upper Credit**: CGPA >= 3.0
- **Lower Credit**: CGPA >= 2.5
- **Pass**: CGPA >= 2.0

## Environment Variables

```bash
# Database
DB_NAME=university_portal
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# University Configuration
ACADEMIC_STYLE=british_nigerian  # or american
SYSTEM_TYPE=university  # or polytechnic
UNIVERSITY_NAME=University of Nigeria
UNIVERSITY_SHORT=UNN

# Payment Gateways (Nigerian)
REMITA_KEY=your_remita_key
PAYSTACK_SECRET=your_paystack_secret
FLUTTERWAVE_SECRET=your_flutterwave_secret

# Security
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
```

## Features by System

| Feature | British/Nigerian | American | Polytechnic |
|---------|-----------------|----------|-------------|
| JAMB Integration | ✅ | ❌ | ✅ |
| CAPS Sync | ✅ | ❌ | ✅ |
| SAT/ACT | ❌ | ✅ | ❌ |
| TETFund | ✅ | ❌ | ❌ |
| NBTE | ❌ | ❌ | ✅ |
| SIWES | ✅ | ❌ | ✅ |
| Major/Minor | ❌ | ✅ | ❌ |
| Liberal Arts | ❌ | ✅ | ❌ |
| Thesis | ✅ | ✅ | ✅ |
| HND/ND | ❌ | ❌ | ✅ |

## License

MIT