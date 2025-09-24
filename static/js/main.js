// ExpenseTracker - Main JavaScript File
// CRED-Inspired Interactive Features

class ExpenseTracker {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initAnimations();
        this.setupFormValidation();
        this.initThemeToggle();
        this.setupNotifications();
        this.initServiceWorker();
    }

    setupEventListeners() {
        // Mobile menu toggle
        const menuToggle = document.querySelector('.mobile-menu-toggle');
        const navLinks = document.querySelector('.nav-links');
        
        if (menuToggle) {
            menuToggle.addEventListener('click', () => {
                navLinks.classList.toggle('active');
                menuToggle.classList.toggle('active');
            });
        }

        // Close mobile menu on link click
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (navLinks) {
                    navLinks.classList.remove('active');
                }
                if (menuToggle) {
                    menuToggle.classList.remove('active');
                }
            });
        });

        // Flash message auto-hide
        setTimeout(() => {
            document.querySelectorAll('.flash-message').forEach(flash => {
                flash.style.opacity = '0';
                flash.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    flash.remove();
                }, 300);
            });
        }, 5000);

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Auto-resize textareas
        document.querySelectorAll('textarea').forEach(textarea => {
            textarea.addEventListener('input', this.autoResize);
            this.autoResize.call(textarea);
        });

        // Number input formatting
        document.querySelectorAll('input[type="number"]').forEach(input => {
            input.addEventListener('input', this.formatNumberInput);
        });

        // Form auto-save
        this.setupAutoSave();
    }

    autoResize() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    }

    formatNumberInput(e) {
        let value = e.target.value;
        
        // Remove any non-digit characters except decimal point
        value = value.replace(/[^0-9.]/g, '');
        
        // Ensure only one decimal point
        const parts = value.split('.');
        if (parts.length > 2) {
            value = parts[0] + '.' + parts.slice(1).join('');
        }
        
        // Limit to 2 decimal places
        if (parts[1] && parts[1].length > 2) {
            value = parts[0] + '.' + parts[1].substring(0, 2);
        }
        
        e.target.value = value;
    }

    initAnimations() {
        // Intersection Observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe elements that should animate
        document.querySelectorAll('.feature-card, .stat-card, .expense-item, .expense-card').forEach(el => {
            observer.observe(el);
        });

        // Parallax effect for hero section
        const hero = document.querySelector('.hero-section');
        if (hero) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;
                hero.style.transform = `translateY(${rate}px)`;
            });
        }

        // Floating animation for demo cards
        this.setupFloatingAnimation();
    }

    setupFloatingAnimation() {
        const floatingElements = document.querySelectorAll('.expense-card-demo');
        
        floatingElements.forEach((element, index) => {
            // Random floating animation
            const duration = 3000 + Math.random() * 2000;
            const delay = index * 500;
            
            element.style.animationDuration = `${duration}ms`;
            element.style.animationDelay = `${delay}ms`;
        });
    }

    setupFormValidation() {
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                    this.showFormErrors(form);
                }
            });

            // Real-time validation
            form.querySelectorAll('input, textarea, select').forEach(field => {
                field.addEventListener('blur', () => this.validateField(field));
                field.addEventListener('input', () => this.clearFieldError(field));
            });
        });
    }

    validateForm(form) {
        let isValid = true;
        const fields = form.querySelectorAll('input[required], textarea[required], select[required]');
        
        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';

        // Required validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'This field is required';
        }

        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                message = 'Please enter a valid email address';
            }
        }

        // Password validation
        if (field.type === 'password' && value) {
            if (value.length < 6) {
                isValid = false;
                message = 'Password must be at least 6 characters long';
            }
        }

        // Number validation
        if (field.type === 'number' && value) {
            const num = parseFloat(value);
            if (isNaN(num) || num < 0) {
                isValid = false;
                message = 'Please enter a valid positive number';
            }
        }

        // Amount validation (specific for expense amount)
        if (field.name === 'amount' && value) {
            const amount = parseFloat(value);
            if (amount > 1000000) {
                isValid = false;
                message = 'Amount cannot exceed ₹10,00,000';
            }
        }

        this.showFieldValidation(field, isValid, message);
        return isValid;
    }

    showFieldValidation(field, isValid, message) {
        const errorElement = field.parentElement.querySelector('.field-error') || 
                            this.createErrorElement(field);

        if (isValid) {
            field.classList.remove('error');
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        } else {
            field.classList.add('error');
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    }

    createErrorElement(field) {
        const errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.style.cssText = `
            color: var(--error-color);
            font-size: 0.8rem;
            margin-top: 0.25rem;
            display: none;
        `;
        field.parentElement.appendChild(errorElement);
        return errorElement;
    }

    clearFieldError(field) {
        field.classList.remove('error');
        const errorElement = field.parentElement.querySelector('.field-error');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }

    showFormErrors(form) {
        const firstErrorField = form.querySelector('.error');
        if (firstErrorField) {
            firstErrorField.focus();
            firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    initThemeToggle() {
        // Future implementation for light/dark theme toggle
        const savedTheme = localStorage.getItem('expense-tracker-theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
    }

    setupNotifications() {
        // Request notification permission if supported
        if ('Notification' in window && navigator.serviceWorker) {
            Notification.requestPermission();
        }
    }

    initServiceWorker() {
        // Register service worker for offline functionality
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then(registration => {
                        console.log('SW registered: ', registration);
                    })
                    .catch(registrationError => {
                        console.log('SW registration failed: ', registrationError);
                    });
            });
        }
    }

    setupAutoSave() {
        const forms = document.querySelectorAll('form[data-auto-save]');
        
        forms.forEach(form => {
            const formId = form.id || 'default-form';
            
            // Load saved data
            this.loadFormData(form, formId);
            
            // Save on input
            form.addEventListener('input', (e) => {
                this.debounce(() => this.saveFormData(form, formId), 1000)();
            });
            
            // Clear saved data on successful submit
            form.addEventListener('submit', () => {
                localStorage.removeItem(`form-data-${formId}`);
            });
        });
    }

    saveFormData(form, formId) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        localStorage.setItem(`form-data-${formId}`, JSON.stringify(data));
        this.showAutoSaveIndicator();
    }

    loadFormData(form, formId) {
        const savedData = localStorage.getItem(`form-data-${formId}`);
        
        if (savedData) {
            const data = JSON.parse(savedData);
            
            Object.keys(data).forEach(key => {
                const field = form.querySelector(`[name="${key}"]`);
                if (field && !field.value) {
                    field.value = data[key];
                }
            });
        }
    }

    showAutoSaveIndicator() {
        let indicator = document.querySelector('.auto-save-indicator');
        
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'auto-save-indicator';
            indicator.innerHTML = '💾 Draft saved';
            indicator.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: var(--success-color);
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 0.8rem;
                z-index: 1000;
                opacity: 0;
                transition: opacity 0.3s ease;
            `;
            document.body.appendChild(indicator);
        }
        
        indicator.style.opacity = '1';
        
        setTimeout(() => {
            indicator.style.opacity = '0';
        }, 2000);
    }

    debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }

    // Utility functions
    static formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 2
        }).format(amount);
    }

    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    static formatTime(timeString) {
        const [hours, minutes] = timeString.split(':');
        const time = new Date();
        time.setHours(hours, minutes);
        return time.toLocaleTimeString('en-IN', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
    }

    // Chart utilities (for future implementation)
    static initCharts() {
        // Placeholder for chart initialization
        console.log('Charts will be implemented in future version');
    }
}

// Expense specific functions
class ExpenseManager {
    constructor() {
        this.setupExpenseSpecificFeatures();
    }

    setupExpenseSpecificFeatures() {
        // Quick add functionality
        this.setupQuickAdd();
        
        // Category selection
        this.setupCategorySelection();
        
        // Amount suggestions
        this.setupAmountSuggestions();
        
        // Search and filter
        this.setupSearchAndFilter();
        
        // Export functionality
        this.setupExportFeatures();
    }

    setupQuickAdd() {
        document.querySelectorAll('.quick-add-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const data = btn.dataset;
                this.fillExpenseForm(data);
            });
        });
    }

    fillExpenseForm(data) {
        if (data.amount) {
            const amountField = document.getElementById('amount');
            if (amountField) amountField.value = data.amount;
        }
        
        if (data.subject) {
            const subjectField = document.getElementById('subject');
            if (subjectField) subjectField.value = data.subject;
        }
        
        if (data.category) {
            const categoryRadio = document.querySelector(`input[name="category"][value="${data.category}"]`);
            if (categoryRadio) {
                categoryRadio.checked = true;
                categoryRadio.dispatchEvent(new Event('change'));
            }
        }
    }

    setupCategorySelection() {
        document.querySelectorAll('input[name="category"]').forEach(radio => {
            radio.addEventListener('change', () => {
                // Remove selected class from all options
                document.querySelectorAll('.category-option').forEach(option => {
                    option.classList.remove('selected');
                });
                
                // Add selected class to current option
                radio.closest('.category-option').classList.add('selected');
            });
        });
    }

    setupAmountSuggestions() {
        document.querySelectorAll('.amount-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const amount = btn.getAttribute('data-amount');
                const amountField = document.getElementById('amount');
                if (amountField) {
                    amountField.value = amount;
                    amountField.focus();
                    
                    // Add visual feedback
                    btn.classList.add('selected');
                    setTimeout(() => btn.classList.remove('selected'), 200);
                }
            });
        });
    }

    setupSearchAndFilter() {
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filterExpenses(e.target.value);
            });
        }
    }

    filterExpenses(searchTerm) {
        const term = searchTerm.toLowerCase();
        const expenseCards = document.querySelectorAll('.expense-card');
        
        expenseCards.forEach(card => {
            const title = card.querySelector('.expense-title')?.textContent.toLowerCase() || '';
            const description = card.querySelector('.expense-description')?.textContent.toLowerCase() || '';
            const category = card.querySelector('.expense-category')?.textContent.toLowerCase() || '';
            
            const matches = title.includes(term) || 
                           description.includes(term) || 
                           category.includes(term);
            
            card.style.display = matches ? 'block' : 'none';
        });
    }

    setupExportFeatures() {
        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportToCSV();
            });
        }
    }

    exportToCSV() {
        const expenses = this.getExpenseData();
        const csv = this.convertToCSV(expenses);
        this.downloadCSV(csv);
    }

    getExpenseData() {
        const expenses = [];
        document.querySelectorAll('.expense-card').forEach(card => {
            const expense = {
                date: card.querySelector('.expense-date')?.textContent || '',
                time: card.querySelector('.expense-time')?.textContent || '',
                title: card.querySelector('.expense-title')?.textContent || '',
                category: card.querySelector('.expense-category')?.textContent || '',
                amount: card.querySelector('.amount-value')?.textContent || '',
                description: card.querySelector('.expense-description')?.textContent || ''
            };
            expenses.push(expense);
        });
        return expenses;
    }

    convertToCSV(data) {
        const headers = ['Date', 'Time', 'Title', 'Category', 'Amount', 'Description'];
        const csvContent = [
            headers.join(','),
            ...data.map(row => 
                headers.map(header => 
                    `"${row[header.toLowerCase()] || ''}"`
                ).join(',')
            )
        ].join('\\n');
        
        return csvContent;
    }

    downloadCSV(csv) {
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        
        a.href = url;
        a.download = `expenses_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        window.URL.revokeObjectURL(url);
        
        // Show success message
        this.showToast('Expenses exported successfully!', 'success');
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: var(--${type === 'success' ? 'success' : 'primary'}-color);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 1000;
            animation: slideInRight 0.3s ease-out;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Dashboard specific functionality
class Dashboard {
    constructor() {
        this.setupDashboard();
    }

    setupDashboard() {
        this.animateStats();
        this.setupRefresh();
        this.initRealTimeUpdates();
    }

    animateStats() {
        document.querySelectorAll('.stat-value').forEach(stat => {
            const finalValue = stat.textContent;
            const numericValue = parseFloat(finalValue.replace(/[^0-9.-]+/g, ''));
            
            if (!isNaN(numericValue)) {
                this.countUp(stat, numericValue, finalValue);
            }
        });
    }

    countUp(element, target, originalText) {
        const duration = 2000; // 2 seconds
        const startTime = Date.now();
        const prefix = originalText.substring(0, originalText.search(/\\d/));
        const suffix = originalText.substring(originalText.search(/\\d/) + target.toString().length);
        
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.floor(target * this.easeOutQuart(progress));
            element.textContent = prefix + current.toLocaleString('en-IN') + suffix;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }

    easeOutQuart(t) {
        return 1 - (--t) * t * t * t;
    }

    setupRefresh() {
        // Add pull-to-refresh functionality for mobile
        let startY = 0;
        let pullDistance = 0;
        const threshold = 60;
        
        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].pageY;
            }
        });
        
        document.addEventListener('touchmove', (e) => {
            if (startY > 0) {
                pullDistance = e.touches[0].pageY - startY;
                if (pullDistance > 0) {
                    e.preventDefault();
                    // Add visual feedback here
                }
            }
        });
        
        document.addEventListener('touchend', () => {
            if (pullDistance > threshold) {
                this.refreshData();
            }
            startY = 0;
            pullDistance = 0;
        });
    }

    refreshData() {
        // Simulate data refresh
        this.showToast('Refreshing data...', 'info');
        
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }

    initRealTimeUpdates() {
        // Future implementation for real-time updates via WebSocket
        console.log('Real-time updates will be implemented in future version');
    }

    showToast(message, type) {
        const toast = document.createElement('div');
        toast.textContent = message;
        toast.className = `flash-message flash-${type}`;
        
        const container = document.querySelector('.flash-container') || document.body;
        container.appendChild(toast);
        
        setTimeout(() => toast.remove(), 3000);
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize main tracker
    const tracker = new ExpenseTracker();
    
    // Initialize page-specific functionality
    if (document.querySelector('.add-expense-page') || document.querySelector('.view-expenses-page')) {
        const expenseManager = new ExpenseManager();
    }
    
    if (document.querySelector('.dashboard')) {
        const dashboard = new Dashboard();
    }
    
    // Global utility functions
    window.ExpenseTracker = {
        formatCurrency: ExpenseTracker.formatCurrency,
        formatDate: ExpenseTracker.formatDate,
        formatTime: ExpenseTracker.formatTime
    };
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ExpenseTracker, ExpenseManager, Dashboard };
}