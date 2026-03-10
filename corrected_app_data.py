# Corrected data sections for your Flask app.py

# Updated achievements data with correct image paths
achievements_data = [
    {
        'title': 'First Place - Innovation Day Celebration',
        'organization': 'Velagapudi Ramakrishna Siddhartha Engineering College',
        'description': 'Won 1st place for the "Smart Helmet for Coal Mine Workers," an AIoT safety solution for detecting harmful gases in coal mines.',
        'image': 'images/solo.png',  # Fixed: Using existing solo.png
        'emoji': '🥇'
    },
    {
        'title': 'Top 8 Startup and Innovation Ideas',
        'organization': 'AIC ALEAP WE Hub & MSME Minister, Andhra Pradesh',
        'description': 'Recognized for startup idea "Robotics for Bomb Detection and Disposal" at an MSME-sponsored innovation event, received award for best startup idea.',
        'image': 'images/cert.svg',  # Fixed: Using existing cert.svg
        'emoji': '🚀'
    },
    {
        'title': 'Appreciation Award - Innovation Acquisition Summit-24',
        'organization': 'VIT-AP, in collaboration with FAPSIA & NRDC',
        'description': '₹3 lakhs in funding for AIoT-based smart helmet to monitor harmful gases in real-time for coal mine workers\' safety.',
        'image': 'images/vit.png',  # Fixed: Using existing vit.png
        'emoji': '🛡️'
    },
    {
        'title': '₹3 Lakhs Funding',
        'organization': 'Innovation Grant',
        'description': 'Received funding for the development of an AIoT-based smart helmet to monitor harmful gases in real-time for coal mine workers.',
        'image': 'images/awards/funding.svg',  # Using existing funding.svg
        'emoji': '💰'
    }
]

# Updated projects data with correct image paths
project_data = [
    {
        'title': 'Smart Helmet for Coal Mine Workers',
        'emoji': '⛏️',
        'description': 'IoT-based safety solution using Arduino, gas sensors, GPS, and an SMS alert system to detect methane (CH4) and carbon monoxide (CO) in coal mines. Features LoRa/GSM communication for real-time, long-range alerts.',
        'image': 'images/he.png',  # Fixed: Using existing he.png
        'tech': ['Arduino', 'IoT', 'Sensors', 'GSM/LoRa']
    },
    {
        'title': 'Health Insurance Fraud Detection',
        'emoji': '💡',
        'description': 'AI-powered fraud detection for health insurance claims using XGBoost and SVM. Implemented data preprocessing, anomaly detection, and feature engineering, integrated into a web dashboard for real-time analysis.',
        'image': 'images/projects/insurance_fraud.svg',  # Using existing SVG
        'tech': ['Python', 'Machine Learning', 'XGBoost', 'SVM', 'Data Analysis','Hybrid Model']
    },
    {
        'title': 'AI Resume Builder',
        'emoji': '🧾',
        'description': 'Web-based platform for creating professional resumes featuring templates, real-time suggestions, and AI-driven feedback for professionally optimized resumes.',
        'image': 'images/projects/resume_builder.svg',  # Using existing SVG
        'tech': ['HTML/CSS', 'JavaScript', 'Python', 'AI', 'Web Development']
    },
    {
        'title': 'Smart Payroll System',
        'emoji': '💼',
        'description': 'Payroll system using Python (Flask), MySQL, and Bootstrap/Tailwind CSS with role-based authentication, automated payroll processing, and biometric attendance integration.',
        'image': 'images/projects/payroll.svg',  # Using existing SVG
        'tech': ['Flask', 'MySQL', 'Bootstrap', 'Python', 'Authentication']
    }
]

# Updated gallery images with correct paths and responsive classes
gallery_images = [
    {
        'src': 'images/he.png', 
        'alt': 'Smart Helmet Project for Coal Mine Workers Safety', 
        'caption': 'Smart Helmet for Coal Miners',
        'class': 'img-fluid'
    },
    {
        'src': 'images/projects/insurance_fraud.svg', 
        'alt': 'Health Insurance Fraud Detection AI System', 
        'caption': 'Health Insurance Fraud Detection',
        'class': 'img-fluid'
    },
    {
        'src': 'images/projects/resume_builder.svg', 
        'alt': 'AI-Powered Resume Builder Platform', 
        'caption': 'AI Resume Builder Tool',
        'class': 'img-fluid'
    },
    {
        'src': 'images/projects/payroll.svg', 
        'alt': 'Advanced Smart Payroll Management System', 
        'caption': 'Advanced Smart Payroll System',
        'class': 'img-fluid'
    },
    {
        'src': 'images/awards/first_prize.svg', 
        'alt': 'First Prize Award for Innovation', 
        'caption': 'Innovation Day First Prize',
        'class': 'img-fluid'
    },
    {
        'src': 'images/awards/startup.svg', 
        'alt': 'Top 8 Startup Recognition Award', 
        'caption': 'Top 8 Startup Recognition',
        'class': 'img-fluid'
    },
    {
        'src': 'images/awards/vit_ap.svg', 
        'alt': 'VIT-AP Innovation Acquisition Award', 
        'caption': 'Innovation Acquisition Award',
        'class': 'img-fluid'
    },
    {
        'src': 'images/awards/funding.svg', 
        'alt': 'Funding Grant Award Certificate', 
        'caption': '₹3 Lakhs Funding Grant',
        'class': 'img-fluid'
    }
]