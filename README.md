# srinivas_profile
A modern, responsive portfolio website showcasing AI/ML projects, achievements, and professional journey. Built with Flask, Bootstrap 5, and featuring an interactive gallery with modal popups, contact form with email notifications, and production-ready Docker deployment


# Srinivasa Rao Talari - Professional Portfolio

A modern, responsive portfolio website showcasing projects, achievements, and professional journey in AI/ML development, IoT, and full-stack engineering.

## 🚀 Features

- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Interactive Gallery**: Full-screen modal popup for images
- **Project Showcase**: Detailed project descriptions with tech stacks
- **Achievements Section**: Awards and recognition display
- **Contact Form**: Functional contact with email notifications
- **Newsletter Subscription**: Email subscription system
- **Dark Theme**: Professional dark theme design
- **Smooth Animations**: AOS (Animate On Scroll) effects
- **Production Ready**: Docker support, environment-based configuration

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Animation**: AOS (Animate On Scroll), Typed.js, Particles.js
- **Email**: Flask-Mail with SMTP
- **Forms**: Flask-WTF with CSRF protection
- **Deployment**: Docker, Gunicorn
- **Development**: Python 3.11+

## 📦 Installation

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/srinivas_profile.git
   cd srinivas_profile
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

   Visit `http://localhost:5000` to view the portfolio.

## 🌐 Deployment

### Development
```bash
python app.py
```

### Production
```bash
python run_production.py
```

### Docker
```bash
docker-compose up --build
```

## ⚙️ Configuration

Key environment variables:

```bash
FLASK_CONFIG=production          # or development
SECRET_KEY=your-secret-key       # Required for production
MAIL_SERVER=smtp.gmail.com       # Email server
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
RESUME_FILENAME=resume.docx      # Resume file name
```

## 📁 Project Structure

```
srinivas_profile/
├── app.py                    # Main Flask application
├── config.py                 # Configuration classes
├── forms.py                  # WTForms classes
├── run_production.py         # Production server script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   ├── images/
│   └── files/
└── templates/               # HTML templates
    ├── base.html
    ├── index.html
    ├── about.html
    ├── projects.html
    ├── achievements.html
    ├── certifications.html
    ├── gallery.html
    ├── contact.html
    ├── resume.html
    ├── 404.html
    └── 500.html
```

## 🎨 Sections

- **Home**: Hero section with animated text and particles
- **About**: Personal introduction and skills
- **Projects**: Showcase of technical projects
- **Achievements**: Awards and recognitions
- **Certifications**: Professional certifications
- **Gallery**: Visual portfolio with modal popup
- **Contact**: Contact form and newsletter subscription
- **Resume**: Resume download functionality

## 🔒 Security Features

- CSRF protection on all forms
- Secure session cookies
- Environment-based configuration
- Input validation and sanitization
- Error handling and logging

## 📱 Mobile Responsive

The portfolio is fully responsive and works seamlessly on:
- Desktop (1920x1080 and above)
- Laptop (1366x768 and above)
- Tablet (768x1024 and above)
- Mobile (320x568 and above)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Srinivasa Rao Talari**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: srininvast20@gmail.com
- Portfolio: [https://your-portfolio-url.com](https://your-portfolio-url.com)

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [AOS](https://michalsnik.github.io/aos/) - Animation library
- [Font Awesome](https://fontawesome.com/) - Icon library

---

⭐ If you like this portfolio, please give it a star!
