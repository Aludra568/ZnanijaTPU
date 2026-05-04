// --- ИНИЦИАЛИЗАЦИЯ ДАННЫХ ---
let questions = JSON.parse(localStorage.getItem('questions')) || [];
let currentUser = localStorage.getItem('currentUser') || null;
let currentQuestionId = null;
let activeFilter = 'all';

// Полный список дисциплин
const allSubjects = [
    "Математика 1.3", "Математика 2.1", "Математика 2.6",
    "Физика 1.1", "Физика 1.2", "Механика",
    "Java", "Python", "C++",
    "Начертательная геометрия", "Химия", "История России", 
    "Основы государственности", "Иностранный язык", "Философия", "Экономика"
];

window.onload = () => {
    populateSubjectSelect();
    if (currentUser) {
        showApp();
    }
};

// Заполнение селектора в форме вопроса
function populateSubjectSelect() {
    const select = document.getElementById('q-subject');
    if (select) {
        select.innerHTML = ''; 
        allSubjects.forEach(subject => {
            const option = document.createElement('option');
            option.value = subject;
            option.innerText = subject;
            select.appendChild(option);
        });
    }
}

// --- ФУНКЦИИ АВТОРИЗАЦИИ ---
function login() {
    const userField = document.getElementById('login-username');
    if (!userField) return;

    const user = userField.value;
    if (user.trim().length > 2) {
        currentUser = user.trim();
        localStorage.setItem('currentUser', currentUser);
        showApp();
    } else {
        const error = document.getElementById('auth-error');
        if (error) error.innerText = "Введите имя (минимум 3 символа)";
    }
}

function logout() {
    localStorage.removeItem('currentUser');
    location.reload();
}

function showApp() {
    const viewAuth = document.getElementById('view-auth');
    const viewApp = document.getElementById('view-app');
    const displayUser = document.getElementById('display-username');

    if (viewAuth) viewAuth.style.display = 'none';
    if (viewApp) viewApp.style.display = 'block';
    if (displayUser) displayUser.innerText = currentUser;
    
    renderQuestions();
}

// --- РАБОТА С ВОПРОСАМИ ---
function renderQuestions(filter = activeFilter, search = '') {
    activeFilter = filter;
    const list = document.getElementById('questions-list');
    if (!list) return;
    list.innerHTML = '';

    const filtered = questions.filter(q => {
        const matchesSubject = filter === 'all' || q.subject === filter;
        const matchesSearch = q.title.toLowerCase().includes(search.toLowerCase());
        return matchesSubject && matchesSearch;
    });

    if (filtered.length === 0) {
        list.innerHTML = '<p style="text-align:center; color:#999; padding:20px;">Вопросов пока нет</p>';
        return;
    }

    filtered.forEach(q => {
        const hasFile = q.fileName ? ` | <i class="fa fa-paperclip"></i> ${q.fileName}` : '';
        list.innerHTML += `
            <div class="question-card" onclick="showQuestionDetail(${q.id})">
                <div class="card-header">
                    <span class="badge default-badge">${q.subject}</span>
                    <span style="color:#999; font-size:0.8rem">${q.date}</span>
                </div>
                <h3>${q.title}</h3>
                <p style="color:#666; margin: 10px 0;">${q.text.substring(0, 100)}...</p>
                <div style="font-size:0.9rem; color:#888; border-top: 1px solid #f5f5f5; padding-top:10px;">
                    <i class="fa fa-comment"></i> ${q.answers.length} ответов | Автор: ${q.author}${hasFile}
                </div>
            </div>
        `;
    });
}

// Функции для работы с формой и файлами
function toggleAddForm() {
    const form = document.getElementById('add-question-form');
    if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function updateFileName(displayId, input) {
    const display = document.getElementById(displayId);
    if (display && input.files.length > 0) {
        display.innerText = input.files[0].name;
    }
}

function saveQuestion() {
    const titleInput = document.getElementById('q-title');
    const textInput = document.getElementById('q-text');
    const subjInput = document.getElementById('q-subject');
    const fileInput = document.getElementById('q-file');

    if (titleInput && textInput && titleInput.value && textInput.value) {
        const newQ = {
            id: Date.now(),
            author: currentUser,
            subject: subjInput ? subjInput.value : "Общее",
            title: titleInput.value,
            text: textInput.value,
            date: new Date().toLocaleDateString(),
            fileName: (fileInput && fileInput.files.length > 0) ? fileInput.files[0].name : null,
            answers: []
        };
        
        questions.unshift(newQ);
        localStorage.setItem('questions', JSON.stringify(questions));
        
        // Очистка
        titleInput.value = '';
        textInput.value = '';
        if (fileInput) fileInput.value = '';
        const fileDisplay = document.getElementById('q-file-name');
        if (fileDisplay) fileDisplay.innerText = '';
        
        toggleAddForm();
        renderQuestions();
    }
}

// --- ДЕТАЛИ И ОТВЕТЫ ---
function showQuestionDetail(id) {
    currentQuestionId = id;
    const q = questions.find(q => q.id === id);
    if (!q) return;
    
    const qSection = document.getElementById('questions-section');
    const dSection = document.getElementById('detail-section');
    const content = document.getElementById('full-question-content');

    if (qSection) qSection.style.display = 'none';
    if (dSection) dSection.style.display = 'block';
    
    const fileHtml = q.fileName ? `<div style="margin: 10px 0; color: #8a2be2;"><i class="fa fa-file-alt"></i> Файл: ${q.fileName}</div>` : '';
    
    if (content) {
        content.innerHTML = `
            <span class="badge default-badge">${q.subject}</span>
            <h2 style="margin:10px 0">${q.title}</h2>
            <p style="font-size:1.1rem; line-height:1.6">${q.text}</p>
            ${fileHtml}
            <p style="margin-top:15px; color:#888">Автор: ${q.author} (${q.date})</p>
        `;
    }
    renderAnswers(q);
}

function renderAnswers(q) {
    const list = document.getElementById('answers-list');
    if (!list) return;

    list.innerHTML = q.answers.length ? '<h4>Ответы:</h4>' : '<p style="color:#999">Ответов пока нет.</p>';
    
    q.answers.forEach(a => {
        const aFile = a.fileName ? `<div style="color: #8a2be2; font-size: 0.8rem;"><i class="fa fa-paperclip"></i> ${a.fileName}</div>` : '';
        list.innerHTML += `
            <div class="question-card" style="background:#fcfaff; cursor:default; margin-top: 10px;">
                <p>${a.text}</p>
                ${aFile}
                <small style="color:#888">Ответил: ${a.author} (${a.date})</small>
            </div>
        `;
    });
}

function saveAnswer() {
    const textInput = document.getElementById('a-text');
    const fileInput = document.getElementById('a-file');
    
    if (textInput && textInput.value) {
        const qIndex = questions.findIndex(q => q.id === currentQuestionId);
        if (qIndex !== -1) {
            questions[qIndex].answers.push({
                author: currentUser,
                text: textInput.value,
                date: new Date().toLocaleDateString(),
                fileName: (fileInput && fileInput.files.length > 0) ? fileInput.files[0].name : null
            });
            
            localStorage.setItem('questions', JSON.stringify(questions));
            textInput.value = '';
            if (fileInput) fileInput.value = '';
            const fileDisplay = document.getElementById('a-file-name');
            if (fileDisplay) fileDisplay.innerText = '';
            
            renderAnswers(questions[qIndex]);
        }
    }
}

// --- НАВИГАЦИЯ ---
function showMainSection() {
    const qSection = document.getElementById('questions-section');
    const dSection = document.getElementById('detail-section');
    if (qSection) qSection.style.display = 'block';
    if (dSection) dSection.style.display = 'none';
    renderQuestions();
}

function filterBySubject(subject) {
    const items = document.querySelectorAll('.sidebar li');
    items.forEach(li => {
        li.classList.remove('active');
        li.classList.remove('active-sub');
    });

    // Безопасное получение элемента, по которому кликнули
    const clickedElement = window.event ? window.event.currentTarget : null;
    if (clickedElement) {
        clickedElement.classList.add(subject === 'all' ? 'active' : 'active-sub');
    }
    
    const title = document.getElementById('section-title');
    if (title) title.innerText = subject === 'all' ? 'Последние вопросы' : subject;
    
    renderQuestions(subject);
}

function searchQuestions() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) renderQuestions(activeFilter, searchInput.value);
}

function toggleSubmenu(id) {
    const submenu = document.getElementById(id);
    if (!submenu) return;
    const isVisible = submenu.style.display === 'block';
    document.querySelectorAll('.submenu').forEach(el => el.style.display = 'none');
    submenu.style.display = isVisible ? 'none' : 'block';
}