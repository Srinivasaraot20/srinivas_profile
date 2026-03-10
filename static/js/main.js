// Main JavaScript file for Srinivasa's Portfolio

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animations
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        mirror: false
    });

    // Initialize Particles.js for background effect
    if (document.getElementById('particles-js')) {
        try {
            particlesJS('particles-js', {
                "particles": {
                    "number": {
                        "value": 80,
                        "density": {
                            "enable": true,
                            "value_area": 800
                        }
                    },
                    "color": {
                        "value": "#3a9bdc"
                    },
                    "shape": {
                        "type": "circle",
                        "stroke": {
                            "width": 0,
                            "color": "#000000"
                        },
                        "polygon": {
                            "nb_sides": 5
                        }
                    },
                    "opacity": {
                        "value": 0.5,
                        "random": false,
                        "anim": {
                            "enable": false,
                            "speed": 1,
                            "opacity_min": 0.1,
                            "sync": false
                        }
                    },
                    "size": {
                        "value": 3,
                        "random": true,
                        "anim": {
                            "enable": false,
                            "speed": 40,
                            "size_min": 0.1,
                            "sync": false
                        }
                    },
                    "line_linked": {
                        "enable": true,
                        "distance": 150,
                        "color": "#2c7cb7",
                        "opacity": 0.4,
                        "width": 1
                    },
                    "move": {
                        "enable": true,
                        "speed": 4,
                        "direction": "none",
                        "random": false,
                        "straight": false,
                        "out_mode": "out",
                        "bounce": false,
                        "attract": {
                            "enable": false,
                            "rotateX": 600,
                            "rotateY": 1200
                        }
                    }
                },
                "interactivity": {
                    "detect_on": "canvas",
                    "events": {
                        "onhover": {
                            "enable": true,
                            "mode": "grab"
                        },
                        "onclick": {
                            "enable": true,
                            "mode": "push"
                        },
                        "resize": true
                    },
                    "modes": {
                        "grab": {
                            "distance": 140,
                            "line_linked": {
                                "opacity": 1
                            }
                        },
                        "bubble": {
                            "distance": 400,
                            "size": 40,
                            "duration": 2,
                            "opacity": 8,
                            "speed": 3
                        },
                        "repulse": {
                            "distance": 200,
                            "duration": 0.4
                        },
                        "push": {
                            "particles_nb": 4
                        },
                        "remove": {
                            "particles_nb": 2
                        }
                    }
                },
                "retina_detect": true
            });
        } catch (error) {
            console.log("Particles.js initialization error:", error);
            // Fallback: Apply a subtle gradient background to the element
            const particlesElement = document.getElementById('particles-js');
            if (particlesElement) {
                particlesElement.style.background = "linear-gradient(135deg, #1c3754 0%, #0f2133 100%)";
            }
        }
    }

    // Initialize Typed.js for home page
    if (document.querySelector('.typed-text')) {
        let typed = new Typed('.typed-text', {
            strings: [
                "Hi, I'm Srinivasa Rao 👋",
                "AI/ML Developer",
                "IoT Builder",
                "Full-Stack Intern"
            ],
            typeSpeed: 50,
            backSpeed: 30,
            backDelay: 2000,
            startDelay: 1000,
            loop: true
        });
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Initialize skill bar animations
    const skillBars = document.querySelectorAll('.skill-progress');
    if (skillBars.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const width = target.getAttribute('data-width');
                    target.style.width = width + '%';
                    observer.unobserve(target);
                }
            });
        }, observerOptions);

        skillBars.forEach(bar => {
            observer.observe(bar);
        });
    }

    // Project card flip effect
    const projectCards = document.querySelectorAll('.project-card');
    if (projectCards.length > 0) {
        projectCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.classList.add('flip');
            });
            card.addEventListener('mouseleave', function() {
                this.classList.remove('flip');
            });
        });
    }

    // Gallery lightbox is now handled in gallery.html template

    // Scroll to top button
    const scrollTopBtn = document.getElementById('scroll-top-btn');
    if (scrollTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                scrollTopBtn.classList.add('show');
            } else {
                scrollTopBtn.classList.remove('show');
            }
        });
        
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Intersection Observer for fade-in animations
    const fadeElements = document.querySelectorAll('.fade-up');
    if (fadeElements.length > 0) {
        const fadeObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('appear');
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        fadeElements.forEach(element => {
            fadeObserver.observe(element);
        });
    }

    // Staggered animations
    const staggerItems = document.querySelectorAll('.stagger-item');
    if (staggerItems.length > 0) {
        const staggerObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('appear');
                    staggerObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        staggerItems.forEach(item => {
            staggerObserver.observe(item);
        });
    }

    // Form validation
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            let valid = true;
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const messageInput = document.getElementById('message');
            
            // Reset error messages
            document.querySelectorAll('.invalid-feedback').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
            
            // Validate name
            if (nameInput.value.trim() === '') {
                document.getElementById('name-error').style.display = 'block';
                nameInput.classList.add('is-invalid');
                valid = false;
            }
            
            // Validate email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailInput.value.trim())) {
                document.getElementById('email-error').style.display = 'block';
                emailInput.classList.add('is-invalid');
                valid = false;
            }
            
            // Validate message
            if (messageInput.value.trim() === '') {
                document.getElementById('message-error').style.display = 'block';
                messageInput.classList.add('is-invalid');
                valid = false;
            }
            
            if (!valid) {
                e.preventDefault();
            }
        });
    }
});
