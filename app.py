import os
import logging
import datetime
from pathlib import Path
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory
from flask_mail import Mail, Message
from forms import ContactForm
from config import config

# Initialize Flask app
def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize app with configuration
    config[config_name].init_app(app)
    
    # Configure logging
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    logging.basicConfig(level=log_level)
    
    # Initialize Flask-Mail
    mail = Mail(app)
    
    @app.route('/')
    def index():
        now = datetime.datetime.now()
        return render_template('index.html', title='Home', now=now)

    @app.route('/about')
    def about():
        now = datetime.datetime.now()
        return render_template('about.html', title='About Me', now=now)

    @app.route('/projects')
    def projects():
        now = datetime.datetime.now()
        project_data = [
            {
                'title': 'Smart Helmet for Coal Mine Workers',
                'emoji': '⛏️',
                'description': 'IoT-based safety solution using Arduino, gas sensors, GPS, and an SMS alert system to detect methane (CH4) and carbon monoxide (CO) in coal mines. Features LoRa/GSM communication for real-time, long-range alerts.',
                'image': 'projects/smart_helmet.svg',
                'tech': ['Arduino', 'IoT', 'Sensors', 'GSM/LoRa']
            },
            {
                'title': 'Health Insurance Fraud Detection',
                'emoji': '💡',
                'description': 'AI-powered fraud detection for health insurance claims using XGBoost and SVM. Implemented data preprocessing, anomaly detection, and feature engineering, integrated into a web dashboard for real-time analysis.',
                'image': 'projects/insurance_fraud.svg',
                'tech': ['Python', 'Machine Learning', 'XGBoost', 'SVM', 'Data Analysis','Hybrid Model']
            },
            {
                'title': 'AI Resume Builder',
                'emoji': '🧾',
                'description': 'Web-based platform for creating professional resumes featuring templates, real-time suggestions, and AI-driven feedback for professionally optimized resumes.',
                'image': 'projects/resume_builder.svg',
                'tech': ['HTML/CSS', 'JavaScript', 'Python', 'AI', 'Web Development']
            },
            {
                'title': 'Smart Payroll System',
                'emoji': '💼',
                'description': 'Payroll system using Python (Flask), MySQL, and Bootstrap/Tailwind CSS with role-based authentication, automated payroll processing, and biometric attendance integration.',
                'image': 'projects/payroll.svg',
                'tech': ['Flask', 'MySQL', 'Bootstrap', 'Python', 'Authentication','HTML/CSS','Javascript']
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
                'image': 'awards/solo.png',
                'emoji': '🥇'
            },
            {
                'title': 'Top 8 Startup and Innovation Ideas',
                'organization': 'AIC ALEAP WE Hub & MSME Minister, Andhra Pradesh',
                'description': 'Recognized for startup idea "Robotics for Bomb Detection and Disposal" at an MSME-sponsored innovation event, received award for best startup idea.',
                'image': 'awards/cert.svg',
                'emoji': '🚀'
            },
            {
                'title': 'Appreciation Award - Innovation Acquisition Summit-24',
                'organization': 'VIT-AP, in collaboration with FAPSIA & NRDC',
                'description': '₹3 lakhs in funding for AIoT-based smart helmet to monitor harmful gases in real-time for coal mine workers\' safety.',
                'image': 'awards/vit.png',
                'emoji': '🛡️'
            },
            {
                'title': '₹3 Lakhs Funding',
                'organization': 'Innovation Grant',
                'description': 'Received funding for the development of an AIoT-based smart helmet to monitor harmful gases in real-time for coal mine workers.',
                'image': 'awards/funding.svg',
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
                'organization': 'GalileoX (Universidad Galileo)'
            },
            {
                'title': 'Foundation of R Software',
                'organization': 'IIT Madras (NPTEL)'
            },
             {
                'title': ' ServiceNow Certified System Administrator',
                'organization': 'ServiceNow'
            },
             {
                'title': 'ServiceNow Certified System Administrator',
                'organization': 'ServiceNow'
            },
            {
                'title': 'Artificial Intelligence with Python - Heuristic Search',
                'organization': 'Infysos'
            },
            {
                'title': 'Hardware and Operating Systems',
                'organization': 'IBM'
            },
            {
                'title': 'Introduction to Data Science with Python',
                'organization': 'HarvardX (Harvard University)'
            },
            {
                'title': 'Ethical Hacking',
                'organization': 'IIT Kharagpur (NPTEL)'
            },
            {
                'title': 'NDG Linux Essentials',
                'organization': 'Cisco Networking Academy'
            },
            {
                'title': 'Introduction to Deep Learning',
                'organization': 'Infysos'
            },
            {
                'title': 'Introduction to MongoDB for Students',
                'organization': 'MongoDB'
            },
            {
                'title': 'Production Machine Learning Systems',
                'organization': 'Google Cloud (Coursera)'
            },
            {
                'title': 'Introduction to Networks',
                'organization': 'Cisco Networking Academy'
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
            try:
                msg = Message(
                    subject=f"Portfolio Contact: {form.subject.data}",
                    recipients=[app.config['MAIL_DEFAULT_SENDER']],
                    sender=form.email.data,
                    body=f"""
                    From: {form.name.data} <{form.email.data}>
                    
                    {form.message.data}
                    """
                )
                mail.send(msg)
                flash('Your message has been sent successfully!', 'success')
                return redirect(url_for('contact'))
            except Exception as e:
                app.logger.error(f"Email error: {str(e)}")
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

    @app.errorhandler(404)
    def page_not_found(e):
        now = datetime.datetime.now()
        return render_template('404.html', now=now), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        now = datetime.datetime.now()
        return render_template('500.html', now=now), 500

    return app

# Create app instance for backward compatibility
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


