document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.header__list-link');
    const sections = document.querySelectorAll('main > section');
    const sectionLinks = document.querySelectorAll('a[href^="#"]');

    function showSection(targetId) {
        sections.forEach(section => {
            section.classList.add('hidden');
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
        });

        const targetSection = document.querySelector(targetId);
        if (targetSection) {
            targetSection.classList.remove('hidden');
        }
    }

    sectionLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();

            const targetId = link.getAttribute('href');
            showSection(targetId);

            if (link.classList.contains('header__list-link'))
            {
                link.classList.add('active');
            }
        });
    });

    const API_URL = 'http://127.0.0.1:8000';

    const loginForm = document.querySelector('.login-form');
    const registerForm = document.querySelector('.register-form');

    // Registration
    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.getElementById('reg-username').value;
        const password = document.getElementById('reg-pwd').value;

        try {
            const response = await fetch(`${API_URL}/words/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Registration failed');
            }

            alert('Registration succeed, now you can log in.');
            registerForm.reset();

        } catch (error) {
            alert('Error: ' + error.message);
        }
    });

    // Login
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('pwd').value;

        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch(`${API_URL}/words/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Login failed');
            }

            localStorage.setItem('access_token', data.access_token);

            alert('Login successfully.');
            loginForm.reset();
            showSection('#dictionary-section');

        } catch (error) {
            alert('Error: ' + error.message);
        }
    });

    async function authFetch(endpoint, options = {}) {
        const token = localStorage.getItem('access_token');

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                ...(options.headers || {}),
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            localStorage.removeItem('access_token');
            alert('Session run out of time, log in again.');
            showSection('#auth-section');
            return null;
        }

        return response;
    }

    async function loadProfile() {
        const response = await authFetch('/words/me');
        if (!response || !response.ok) return;

        const user = await response.json();
        console.log(user);
    }

    if (localStorage.getItem('access_token')) {
        loadProfile();
    }
});