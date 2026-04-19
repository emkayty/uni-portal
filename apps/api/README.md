# University Portal - Django Ninja API

## Setup

```bash
cd apps/api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Project Structure

- `models/` - Database models
- `api/` - API endpoints
- `schemas/` - Pydantic schemas
- `services/` - Business logic

## Configuration

Set environment variables:
```bash
export ACADEMIC_STYLE=british_nigerian
export SYSTEM_TYPE=university
```

Or import from config package:
```python
from config.university_config import get_config, BritishNigerianConfig

config = get_config()
```