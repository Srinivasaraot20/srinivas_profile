# Portfolio Website - Production Ready

## Environment Setup

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file with your actual values:**
   - Set a strong `SECRET_KEY`
   - Configure email settings
   - Set `FLASK_CONFIG=production` for production

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

## Production Deployment

### Option 1: Using the production script
```bash
python run_production.py
```

### Option 2: Using Gunicorn directly
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 3: Using Docker (recommended)
```bash
# Build image
docker build -t portfolio .

# Run container
docker run -p 5000:5000 --env-file .env portfolio
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_CONFIG` | Configuration mode | `development` |
| `SECRET_KEY` | Flask secret key | Required for production |
| `PORT` | Server port | `5000` |
| `MAIL_SERVER` | SMTP server | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USERNAME` | Email username | Required |
| `MAIL_PASSWORD` | Email password | Required |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_FILE` | Log file path | `logs/app.log` |

## Security Features

- CSRF protection enabled
- Secure cookies in production
- Environment-based configuration
- No hardcoded paths
- Input validation
- Error handling

## File Structure

```
PersonalPortfolio/
├── app.py                 # Main application
├── config.py             # Configuration classes
├── run_production.py     # Production server script
├── .env.example          # Environment template
├── requirements.txt      # Python dependencies
├── static/              # Static files
├── templates/           # HTML templates
└── logs/               # Log files (created automatically)
```

## Notes

- The application now uses `pathlib.Path` for cross-platform compatibility
- All hardcoded paths have been removed
- Configuration is environment-based
- Resume filename is configurable via environment variables
- Production logging includes rotation and proper formatting
