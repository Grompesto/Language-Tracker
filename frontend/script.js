document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.header__list-link');
    const sections = document.querySelectorAll('main > section');
    const sectionLinks = document.querySelectorAll('a[href^="#"]');

    const protectedSections = ['#dictionary-section', '#profile-section'];

    function showSection(targetId) {
        const token = localStorage.getItem('access_token');
        
        if (protectedSections.includes(targetId) && !token) {
            targetId = '#auth-section';
        } else if (targetId === '#auth-section' && token) {
            targetId = '#dictionary-section';
        }

        sections.forEach(section => section.classList.add('hidden'));
        navLinks.forEach(link => link.classList.remove('active'));

        const targetSection = document.querySelector(targetId);
        if (targetSection) {
            targetSection.classList.remove('hidden');
        }

        const activeLink = document.querySelector(`.header__list-link[href="${targetId}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        if (targetId === '#profile-section' && token) {
            loadProfile();
        } else if (targetId === '#dictionary-section' && token) {
            loadWords();
        }
    }

    sectionLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            showSection(link.getAttribute('href'));
        });
    });

    const initialHash = window.location.hash || '#home-section';
    showSection(initialHash);

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

        document.getElementById('profile-username').textContent = user.username;
        document.getElementById('profile-fullname').textContent = user.full_name || 'Not provided';

        const avatar = document.querySelector('.avatar');
        avatar.textContent = user.username.charAt(0).toUpperCase();
        avatar.style.display = 'flex';
        avatar.style.alightItems = 'center';
        avatar.style.justifyContent = 'center';
        avatar.style.fontSize = '45px';
    }

    if (localStorage.getItem('access_token')) {
        loadProfile();
    }

    const getStartedBtn = document.querySelector('.hero__button');
    getStartedBtn.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('#dictionary-section');
    });

    const logoutBtn = document.querySelector('.profile-container .submit-btn:not(.danger)');
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        alert('You have logged out.')
        showSection('#home-section');
    });

    const deleteAccountBtn = document.querySelector('.profile-container .submit-btn.danger');
    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', async () => {
            const confirmed = confirm('Are you sure you want to delete your account?')
            if (confirmed) {
                const response = await authFetch('/words/me', { method: 'DELETE'});
                if (response && response.ok) {
                    localStorage.removeItem('access_token');
                    alert('Your account has been deleted');
                    showSection('#home-section');
                }
            }
        });
    }

    const addWordBtn = document.getElementById('add-word-btn');

    async function loadWords() {
        const response = await authFetch('/words');
        if (!response || !response.ok) return;

        const words = await response.json();
        const wordList = document.getElementById('word-list');
        wordList.innerHTML = '';

        words.forEach(word => {
            const card = document.createElement('div');
            card.style.padding = '20px';
            card.style.background = 'var(--bg-surface)';
            card.style.borderRadius = 'var(--radius)';
            card.style.boxShadow = 'var(--shadow)';
            card.innerHTML = `
                <h3 style="color: var(--primary); margin-bottom: 10px;">${word.name}</h3>
                <p><strong>Translation:</strong> ${word.translation}</p>
                <p><strong>Difficulty:</strong> ${word.difficulty}</p>
                <div style="margin-top: 15px; display: flex; gap: 10px;">
                    <button class="edit-btn" data-id="${word.id}" data-name="${word.name}" data-trans="${word.translation}" 
                    data-diff="${word.difficulty}" style="background: var(--primary); color: white; border: none; 
                    padding: 5px 15px; border-radius: 5px; cursor: pointer;">Edit</button>
                    <button class="delete-btn" data-id="${word.id}" style="background: #e74c3c; color: white; border: none; 
                    padding: 5px 15px; border-radius: 5px; cursor: pointer;">Delete</button>
                </div>
            `;
            wordList.appendChild(card);
            loadQuizWord();
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const id = e.target.getAttribute('data-id');
                if (confirm('Delete this word?')) {
                    const res = await authFetch(`/words/${id}`, { method: 'DELETE'});
                    if (res && res.ok) loadWords();
                }
            });
        });

        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const id = e.target.getAttribute('data-id');
                const oldName = e.target.getAttribute('data-name');
                const oldTrans = e.target.getAttribute('data-trans');
                const oldDiff = e.target.getAttribute('data-diff');

                const newName = prompt('Edit word:', oldName);
                const newTrans = prompt('Edit translation:', oldTrans);

                if (newName && newTrans) {
                    const res = await authFetch(`/words/${id}`, {
                        method: 'PUT',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            name: newName,
                            translation: newTrans,
                            difficulty: oldDiff,
                            review_count: 0,
                            interval: 1
                        })
                    });
                    if (res && res.ok) loadWords();
                }
            });
        });
    }

    addWordBtn.addEventListener('click', async () => {
        const name = document.getElementById('word-name').value.trim();
        const translation = document.getElementById('word-translation').value.trim();
        const difficulty = document.getElementById('word-difficulty').value;

        if (!name || !translation) {
            alert('Please fill in both the word and translation');
            return;
        }

        const response = await authFetch('/words', {
            method: 'POST',
            headers: {'Content-Type': 'application/json' },
            body: JSON.stringify({
                name,
                translation,
                difficulty,
                review_count: 0,
                interval: 1
            })
        });

        if (response && response.ok) {
            document.getElementById('word-name').value = '';
            document.getElementById('word-translation').value = '';
            loadWords();
        } else if (response) {
            const data = await response.json();
            const errorMsg = Array.isArray(data.detail)
            ? data.detail.map(err => `${err.loc.at(-1)}: ${err.msg}`).join('\n')
            : data.detail;
            alert('Validation Error:\n' + errorMsg);
        }
    });

    let currentQuizWord = null;

    async function loadQuizWord() {
        const response = await authFetch('/words/quiz');
        const wordEl = document.getElementById('quiz-word');
        const transEl = document.getElementById('quiz-translation');
        const showBtn = document.getElementById('btn-show-trans');
        const actions = document.getElementById('quiz-actions');

        if (!response || !response.ok) {
            wordEl.textContent = 'Add some words first!';
            transEl.textContent = '';
            showBtn.style.display = 'none';
            actions.classList.add('hidden');
            return;
        }

        currentQuizWord = await response.json();
        wordEl.textContent = currentQuizWord.name;
        transEl.textContent = currentQuizWord.translation;

        transEl.classList.add('hidden');
        showBtn.style.display = 'inline-block';
        actions.classList.add('hidden');

        document.getElementById('btn-remember').style.backgroundColor = '';
        document.getElementById('btn-forget').style.backgroundColor = '';
        document.getElementById('btn-remember').style.color = 'var(--text-main)';
        document.getElementById('btn-forget').style.color = 'var(--text-main)';
    }

    document.getElementById('btn-show-trans').addEventListener('click', () => {
        document.getElementById('quiz-translation').classList.remove('hidden');
        document.getElementById('btn-show-trans').style.display = 'none';
        document.getElementById('quiz-actions').classList.remove('hidden');
    });

    async function handleReview(remembered) {
        if (!currentQuizWord) return;

        const btn = remembered ? document.getElementById('btn-remember') : document.getElementById('btn-forget');

        btn.style.backgroundColor = remembered ? 'var(--success)' : '#e74c3c';
        btn.style.color = 'white';

        await authFetch(`/words/${currentQuizWord.id}/review?remembered=${remembered}`, {
            method: 'POST'
        });

        setTimeout(() => {
            loadQuizWord();
        }, 500);
    }

    document.getElementById('btn-remember').addEventListener('click', () => handleReview(true));
    document.getElementById('btn-forget').addEventListener('click', () => handleReview(false));
});