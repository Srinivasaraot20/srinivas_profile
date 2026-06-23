import os
import logging
import datetime
import time
import csv
import io
from pathlib import Path
from functools import wraps
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, Response, make_response
from flask_mail import Mail, Message
from forms import ContactForm
from flask_wtf.csrf import CSRFProtect
from config import config
from models import db, ContactMessage
from twilio.rest import Client

# Simple in-memory rate limiter
SUBMISSION_LIMIT = 3
LIMIT_WINDOW = 60
ip_tracker = {}

def is_rate_limited(ip):
    current_time = time.time()
    if ip not in ip_tracker:
        ip_tracker[ip] = []
    ip_tracker[ip] = [t for t in ip_tracker[ip] if current_time - t < LIMIT_WINDOW]
    if len(ip_tracker[ip]) >= SUBMISSION_LIMIT:
        return True
    ip_tracker[ip].append(current_time)
    return False

# Basic Authentication Helper
def check_auth(username, password):
    admin_user = os.environ.get('ADMIN_USER', 'admin')
    admin_pass = os.environ.get('ADMIN_PASS', 'admin123')
    return username == admin_user and password == admin_pass

def authenticate_response():
    return Response(
        'Admin login required.\n'
        'Please authenticate with valid credentials.', 401,
        {'WWW-Authenticate': 'Basic realm="Admin Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate_response()
        return f(*args, **kwargs)
    return decorated

# Twilio WhatsApp Helper
def send_whatsapp_notification(name, email, phone, subject, message, submission_time, admin_phone):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_whatsapp = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
    to_whatsapp = f"whatsapp:+{admin_phone}" if not admin_phone.startswith('whatsapp:') else admin_phone
    
    body = f"""*New Inquiry on Portfolio!* 🚨
*Name:* {name}
*Email:* {email}
*Phone:* {phone}
*Subject:* {subject}
*Message:* {message}
*Time:* {submission_time}"""

    if account_sid and auth_token:
        try:
            client = Client(account_sid, auth_token)
            msg = client.messages.create(
                body=body,
                from_=from_whatsapp,
                to=to_whatsapp
            )
            logging.info(f"WhatsApp notification sent via Twilio: {msg.sid}")
            return True
        except Exception as e:
            logging.error(f"Failed to send WhatsApp notification via Twilio: {str(e)}")
            return False
    else:
        logging.warning("Twilio credentials missing. WhatsApp notification body (logged for testing):")
        logging.warning(body)
        return False


# Initialize Flask app
def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize app with configuration
    config[config_name].init_app(app)
    
    # Initialize CSRF Protection
    csrf = CSRFProtect(app)
    
    # Configure logging
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    logging.basicConfig(level=log_level)
    
    # Initialize Flask-Mail
    mail = Mail(app)
    
    # Initialize Flask-SQLAlchemy
    db.init_app(app)
    
    # Ensure database tables exist
    with app.app_context():
        # Ensure instance directory exists for SQLite
        os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
        db.create_all()
    
    @app.route('/')
    def index():
        now = datetime.datetime.now()
        return render_template('index.html', title='Home', now=now)

    @app.route('/about')
    def about():
        now = datetime.datetime.now()
        return render_template('about.html', title='About Me', now=now)

    @app.route('/skills')
    def skills():
        now = datetime.datetime.now()
        return render_template('skills.html', title='Technical Skills', now=now)

    @app.route('/experience')
    def experience():
        now = datetime.datetime.now()
        return render_template('experience.html', title='Professional Experience', now=now)

    @app.route('/projects')
    def projects():
        now = datetime.datetime.now()
        project_data = [
            {
                'title': 'Smart Helmet for Coal Mine Workers',
                'emoji': '⛏️',
                'description': 'An intelligent IoT-based safety helmet for coal mine workers that continuously monitors hazardous gases, temperature, humidity, and location, sending real-time alerts via LoRa and GSM.',
                'image': 'projects/smart_helmet.svg',
                'tech': ['Arduino Uno', 'ESP32', 'IoT', 'LoRa', 'GSM SIM800L', 'GPS Neo-6M', 'MQ4, MQ135 Gas Sensors', 'DHT11', 'BME680', 'Embedded Systems']
            },
            {
                'title': 'Health Insurance Fraud Detection',
                'emoji': '💡',
                'description': 'An Explainable AI-powered health insurance claim verification and fraud detection system utilizing OCR, NLP, hybrid XGBoost + SVM models, and SHAP explainability.',
                'image': 'projects/insurance_fraud.svg',
                'tech': ['Python', 'Flask', 'Machine Learning', 'XGBoost', 'SVM', 'SHAP', 'NLP', 'OCR (Tesseract)', 'Pandas', 'Scikit-Learn', 'SQLite/MySQL']
            },
            {
                'title': 'AI Resume Builder',
                'emoji': '🧾',
                'description': 'An AI-powered web application that helps users create professional, ATS-friendly resumes with customizable templates, real-time suggestions, and dynamic PDF generation.',
                'image': 'projects/resume_builder.svg',
                'tech': ['HTML5', 'CSS3', 'JavaScript', 'Python', 'Flask', 'AI/NLP', 'Bootstrap', 'SQLite/MySQL', 'PDF Generation', 'Web Development']
            },
            {
                'title': 'Smart Payroll System',
                'emoji': '💼',
                'description': 'Payroll system using Python (Flask), MySQL, and Bootstrap/Tailwind CSS with role-based authentication, automated payroll processing, and biometric attendance integration.',
                'image': 'projects/payroll.svg',
                'tech': ['Flask', 'MySQL', 'Bootstrap', 'Python', 'Authentication','HTML/CSS','Javascript']
            },
            {
                'title': 'Explainable AI Health Insurance Claim Fraud Detection',
                'emoji': '🛡️',
                'description': 'AI-powered health insurance claim fraud detection using Tesseract OCR, BioGPT medical embeddings, RoBERTa transformer classifier, hybrid SMOTE sampling, and SHAP explainability dashboard.',
                'image': 'projects/insurance_fraud.svg',
                'tech': ['Python', 'Flask', 'OCR', 'BioGPT', 'RoBERTa', 'SHAP', 'XGBoost', 'Machine Learning']
            },
            {
                'title': 'A Multi-Stage Deep Learning Framework for Camouflaged Soldier Detection Using UAV Imagery',
                'emoji': '🪖',
                'description': 'UAV surveillance system utilizing RT-DETR object detection and SAM (Segment Anything Model) pixel-level segmentation, integrated with geospatial coordinate mapping on an interactive monitoring dashboard.',
                'image': 'projects/soldier_detection.svg',
                'tech': ['Python', 'Deep Learning', 'PyTorch', 'RT-DETR', 'SAM', 'OpenCV', 'Geospatial Mapping']
            }
        ]
        return render_template('projects.html', title='Projects', projects=project_data, now=now)

    @app.route('/achievements')
    def achievements():
        now = datetime.datetime.now()
        achievements_data = [
            {
                'title': 'First Place - Innovation Day Celebration',
                'organization': 'Velagapudi Ramakrishna Siddhartha Engineering College',
                'description': 'Won 1st place for the "Smart Helmet for Coal Mine Workers," an AIoT safety solution for detecting harmful gases in coal mines.',
                'image': 'solo.png',
                'emoji': '🥇'
            },
            {
                'title': 'Top 8 Startup and Innovation Ideas',
                'organization': 'AIC ALEAP WE Hub & MSME Minister, Andhra Pradesh',
                'description': 'Recognized for startup idea "Robotics for Bomb Detection and Disposal" at an MSME-sponsored innovation event, received award for best startup idea.',
                'image': 'cert.svg',
                'emoji': '🚀'
            },
            {
                'title': 'Appreciation Award - Innovation Acquisition Summit-24',
                'organization': 'VIT-AP, in collaboration with FAPSIA & NRDC',
                'description': '₹3 lakhs in funding for AIoT-based smart helmet to monitor harmful gases in real-time for coal mine workers\' safety.',
                'image': 'vit.png',
                'emoji': '🛡️'
            },
            {
                'title': '₹3 Lakhs Funding',
                'organization': 'Innovation Grant',
                'description': 'Received funding for the development of an AIoT-based smart helmet to monitor harmful gases in real-time for coal mine workers.',
                'image': 'funding.svg',
                'emoji': '💰'
            }
        ]
        return render_template('achievements.html', title='Achievements', achievements=achievements_data, now=now)

    @app.route('/certifications')
    def certifications():
        now = datetime.datetime.now()
        certifications_data = [
            {
                'title': 'Java Programming Fundamentals',
                'organization': 'GalileoX (Universidad Galileo)',
                'image': 'java.svg',
                'link': 'https://credentials.edx.org/'
            },
            {
                'title': 'Foundation of R Software',
                'organization': 'IIT Madras (NPTEL)',
                'image': 'r.svg',
                'link': 'https://nptel.ac.in/'
            },
            {
                'title': 'ServiceNow Certified System Administrator',
                'organization': 'ServiceNow',
                'image': 'servicenow.png',
                'link': 'https://nowlearning.servicenow.com/'
            },
            {
                'title': 'Artificial Intelligence with Python - Heuristic Search',
                'organization': 'Infysos',
                'image': 'ai.svg',
                'link': ''
            },
            {
                'title': 'Hardware and Operating Systems',
                'organization': 'IBM',
                'image': 'hardware.svg',
                'link': 'https://www.coursera.org/'
            },
            {
                'title': 'Introduction to Data Science with Python',
                'organization': 'HarvardX (Harvard University)',
                'image': 'data_science.svg',
                'link': 'https://credentials.edx.org/'
            },
            {
                'title': 'Ethical Hacking',
                'organization': 'IIT Kharagpur (NPTEL)',
                'image': 'ethical_hacking.svg',
                'link': 'https://nptel.ac.in/'
            },
            {
                'title': 'NDG Linux Essentials',
                'organization': 'Cisco Networking Academy',
                'image': 'linux.svg',
                'link': 'https://www.netacad.com/'
            },
            {
                'title': 'Introduction to Deep Learning',
                'organization': 'Infysos',
                'image': 'deep_learning.svg',
                'link': ''
            },
            {
                'title': 'Introduction to MongoDB for Students',
                'organization': 'MongoDB',
                'image': 'mongodb.svg',
                'link': 'https://learn.mongodb.com/'
            },
            {
                'title': 'Production Machine Learning Systems',
                'organization': 'Google Cloud (Coursera)',
                'image': 'ml_systems.svg',
                'link': 'https://www.coursera.org/'
            },
            {
                'title': 'Introduction to Networks',
                'organization': 'Cisco Networking Academy',
                'image': 'networks.svg',
                'link': 'https://www.netacad.com/'
            }
        ]
        return render_template('certifications.html', title='Certifications', certifications=certifications_data, now=now)

    @app.route('/resume')
    def resume():
        now = datetime.datetime.now()
        return render_template('resume.html', title='Resume', now=now)

    @app.route('/download-resume')
    def download_resume():
        try:
            files_folder = app.config.get('FILES_FOLDER', Path(__file__).parent / 'static' / 'files')
            resume_filename = os.environ.get('RESUME_FILENAME', 'Srinivasa Rao Talari_Computer Programmer_20250513.docx')
            resume_path = files_folder / resume_filename
            
            if not resume_path.exists():
                app.logger.error(f"Resume file not found: {resume_path}")
                flash('Resume file not found.', 'error')
                return redirect(url_for('resume'))
            
            return send_from_directory(
                str(files_folder),
                resume_filename,
                as_attachment=True,
                download_name='Srinivasa_Rao_Talari_Resume.docx'
            )
        except Exception as e:
            app.logger.error(f"Error downloading resume: {str(e)}")
            flash('Error downloading resume. Please try again later.', 'error')
            return redirect(url_for('resume'))

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        now = datetime.datetime.now()
        form = ContactForm()
        if form.validate_on_submit():
            visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if visitor_ip and ',' in visitor_ip:
                visitor_ip = visitor_ip.split(',')[0].strip()
            
            # Rate limiting check (max 3 submissions per minute)
            if is_rate_limited(visitor_ip):
                flash('You have exceeded the submission limit. Please wait a minute before trying again.', 'danger')
                return render_template('contact.html', title='Contact Me', form=form, now=now)
                
            try:
                # 1. Store submission in the database permanently
                new_message = ContactMessage(
                    name=form.name.data,
                    email=form.email.data,
                    phone=form.phone.data,
                    subject=form.subject.data,
                    message=form.message.data,
                    ip_address=visitor_ip,
                    status='New'
                )
                db.session.add(new_message)
                db.session.commit()
                
                # 2. Email notification to Admin
                dashboard_url = url_for('admin_dashboard', _external=True)
                admin_msg = Message(
                    subject=f"🚨 New Portfolio Inquiry: {form.subject.data}",
                    recipients=[app.config['ADMIN_EMAIL']],
                    sender=app.config['MAIL_DEFAULT_SENDER']
                )
                admin_msg.html = render_template(
                    'emails/admin_notification.html',
                    name=form.name.data,
                    email=form.email.data,
                    phone=form.phone.data,
                    subject=form.subject.data,
                    message=form.message.data,
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    dashboard_url=dashboard_url
                )
                mail.send(admin_msg)
                
                # 3. Automatic Acknowledgment Email to Visitor
                visitor_msg = Message(
                    subject="Thank you for contacting Srinivasa Rao Talari",
                    recipients=[form.email.data],
                    sender=app.config['MAIL_DEFAULT_SENDER']
                )
                visitor_msg.html = render_template(
                    'emails/visitor_acknowledgment.html',
                    name=form.name.data
                )
                mail.send(visitor_msg)
                
                # 4. WhatsApp notification to Admin
                send_whatsapp_notification(
                    name=form.name.data,
                    email=form.email.data,
                    phone=form.phone.data,
                    subject=form.subject.data,
                    message=form.message.data,
                    submission_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    admin_phone=app.config['ADMIN_WHATSAPP']
                )
                
                flash('Your message has been sent successfully.', 'success')
                return redirect(url_for('contact'))
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Contact form processing error: {str(e)}")
                flash('There was an error sending your message. Please try again later.', 'danger')
        return render_template('contact.html', title='Contact Me', form=form, now=now)

    @app.route('/subscribe', methods=['POST'])
    def subscribe():
        email = request.form.get('email')
        if email:
            try:
                msg = Message(
                    subject="New Newsletter Subscription",
                    recipients=[app.config['MAIL_DEFAULT_SENDER']],
                    body=f"New subscriber: {email}"
                )
                mail.send(msg)
                
                # Send confirmation to subscriber
                welcome_msg = Message(
                    subject="Welcome to Srinivasa Rao Talari's Newsletter",
                    recipients=[email],
                    body="Thank you for subscribing to my newsletter! You'll receive updates about my latest projects and achievements."
                )
                mail.send(welcome_msg)
                
                flash('Thank you for subscribing to my newsletter!', 'success')
            except Exception as e:
                app.logger.error(f"Subscription error: {str(e)}")
                flash('There was an error processing your subscription. Please try again later.', 'danger')
        else:
            flash('Please provide a valid email address.', 'warning')
        
        # Redirect back to the referring page
        referrer = request.referrer or url_for('index')
        return redirect(referrer)

    @app.route('/gallery')
    def gallery():
        now = datetime.datetime.now()
        gallery_images = [
           
            {'src': 'solo.png', 'alt': 'First Prize Award', 'caption': 'Innovation Day First Prize'},
            {'src': 'cert.png', 'alt': 'Startup Award', 'caption': 'Top 8 Startup Recognition'},
            {'src': 'vit.png', 'alt': 'VIT-AP Award', 'caption': 'Innovation Acquisition Award'},
            {'src': 'vitap.jpg', 'alt': 'VIT-AP Award', 'caption': 'VIT-AP Innovation Award'},
            {'src': 'vit-ap.jpg', 'alt': 'VIT-AP Award', 'caption': 'VIT-AP Received Award'},
            {'src': 'fun.jpeg', 'alt': 'Funding Award', 'caption': '₹3 Lakhs Funding Grant'},
            {'src': 'best.jpg', 'alt': 'Best Project Award', 'caption': 'Best Project Award'},
             {'src': 'projects/smart_helmet.svg', 'alt': 'Smart Helmet Project', 'caption': 'Smart Helmet for Coal Miners'},
            {'src': 'projects/insurance_fraud.svg', 'alt': 'Insurance Fraud Detection', 'caption': 'Health Insurance Fraud Detection'},
            {'src': 'projects/resume_builder.svg', 'alt': 'Resume Builder', 'caption': 'AI Resume Builder Tool'},
            {'src': 'projects/payroll.svg', 'alt': 'Payroll System', 'caption': 'Advanced Smart Payroll System'}
        ]
        return render_template('gallery.html', title='Gallery', images=gallery_images, now=now)

    @app.route('/sitemap.xml')
    def sitemap():
        now_date = datetime.datetime.now().strftime('%Y-%m-%d')
        site_url = app.config.get('SITE_URL', 'https://srinivas-profile.onrender.com').rstrip('/')
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site_url}/</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{site_url}/about</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>{site_url}/skills</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>{site_url}/experience</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>{site_url}/projects</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>{site_url}/achievements</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>{site_url}/certifications</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>{site_url}/resume</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>{site_url}/gallery</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>{site_url}/contact</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>"""
        return Response(xml, mimetype='application/xml')

    @app.route('/robots.txt')
    def robots():
        site_url = app.config.get('SITE_URL', 'https://srinivas-profile.onrender.com').rstrip('/')
        txt = f"""User-agent: *
Allow: /
Sitemap: {site_url}/sitemap.xml
"""
        return Response(txt, mimetype='text/plain')

    @app.route('/googled5ad724c92ee2f27.html')
    def google_verification():
        return Response("google-site-verification: googled5ad724c92ee2f27.html", mimetype='text/html')

    @app.errorhandler(404)
    def page_not_found(e):
        now = datetime.datetime.now()
        return render_template('404.html', now=now), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        now = datetime.datetime.now()
        return render_template('500.html', now=now), 500

    @app.route('/admin/messages')
    @requires_auth
    def admin_dashboard():
        now = datetime.datetime.now()
        search_query = request.args.get('search', '').strip()
        status_filter = request.args.get('status', 'All').strip()
        
        # Build query
        query = ContactMessage.query
        
        if status_filter != 'All':
            query = query.filter(ContactMessage.status == status_filter)
            
        if search_query:
            search_pattern = f"%{search_query}%"
            query = query.filter(
                (ContactMessage.name.like(search_pattern)) |
                (ContactMessage.email.like(search_pattern)) |
                (ContactMessage.subject.like(search_pattern)) |
                (ContactMessage.message.like(search_pattern))
            )
            
        # Get statistics (all messages without filters)
        total_count = ContactMessage.query.count()
        new_count = ContactMessage.query.filter(ContactMessage.status == 'New').count()
        read_count = ContactMessage.query.filter(ContactMessage.status == 'Read').count()
        replied_count = ContactMessage.query.filter(ContactMessage.status == 'Replied').count()
        
        stats = {
            'total': total_count,
            'new': new_count,
            'read': read_count,
            'replied': replied_count
        }
        
        # Sort by date descending
        messages_list = query.order_by(ContactMessage.created_at.desc()).all()
        
        return render_template(
            'admin/dashboard.html',
            title='Admin Dashboard',
            messages_list=messages_list,
            stats=stats,
            search_query=search_query,
            status_filter=status_filter,
            now=now
        )

    @app.route('/admin/messages/<int:msg_id>/status/<string:status>', methods=['POST'])
    @requires_auth
    def admin_update_status(msg_id, status):
        if status not in ['New', 'Read', 'Replied']:
            flash('Invalid status value.', 'warning')
            return redirect(url_for('admin_dashboard'))
            
        msg = ContactMessage.query.get_or_404(msg_id)
        msg.status = status
        try:
            db.session.commit()
            flash(f"Message status updated to '{status}'.", 'success')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Failed to update status for message {msg_id}: {str(e)}")
            flash("Failed to update message status.", 'danger')
            
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/messages/<int:msg_id>/delete', methods=['POST'])
    @requires_auth
    def admin_delete_message(msg_id):
        msg = ContactMessage.query.get_or_404(msg_id)
        try:
            db.session.delete(msg)
            db.session.commit()
            flash("Message deleted successfully.", 'success')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Failed to delete message {msg_id}: {str(e)}")
            flash("Failed to delete message.", 'danger')
            
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/messages/export/csv')
    @requires_auth
    def admin_export_csv():
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        
        # Generate CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header row
        writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Subject', 'Message', 'IP Address', 'Date Submitted (UTC)', 'Status'])
        
        # Data rows
        for msg in messages:
            writer.writerow([
                msg.id,
                msg.name,
                msg.email,
                msg.phone,
                msg.subject,
                msg.message,
                msg.ip_address,
                msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                msg.status
            ])
            
        # Create response
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=portfolio_inquiries.csv"
        response.headers["Content-type"] = "text/csv; charset=utf-8"
        return response

    return app

# Create app instance for backward compatibility
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


