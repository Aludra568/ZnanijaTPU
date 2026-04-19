// --- Инициализация начальных данных (Mock DB) ---
const subjectsData = {
    "Математика": ["Математика 1.3", "Математика 2.6", "Математика 3.8"],
    "Физика": ["Физика 1.1", "Физика 2.2", "Физика 3.0"],
    "Иностранные языки": ["Английский A2", "Английский B1", "Немецкий A1"],
    "Информатика и программирование": ["Основы Python", "Алгоритмы и структуры данных", "Веб-разработка"],
    "Начертательная геометрия": ["НГ 1 семестр", "НГ 2 семестр", "Инженерная графика"]
};

// Заполняем localStorage тестовыми данными, если пусто
if (!localStorage.getItem('questions')) {
    const initialQuestions = [
        {
            id: 1,
            subject: "Физика",
            program: "Физика 1.1",
            title: "Закон сохранения импульса",
            text: "Не могу понять задачу про абсолютно неупругое столкновение двух шаров. Как найти конечную скорость?",
            author: "Студент_ТПУ",
            date: new Date().toLocaleDateString(),
            answers: []
        },
        {
            id: 2,
            subject: "Математика",
            program: "Математика 2.6",
            title: "Взятие несобственного интеграла",
            text: "Как доказать сходимость интеграла от 1 до бесконечности (sin x)/x dx?",
            author: "MathLover",
            date: new Date().toLocaleDateString(),
            answers: [
                { text: "Используй признак Дирихле. Синус имеет ограниченную первообразную, а 1/x монотонно стремится к нулю.", file: null, author: "Преподаватель", date: new Date().toLocaleDateString() }
            ]
        }
    ];
    localStorage.setItem('questions', JSON.stringify(initialQuestions));
}

// Текущее состояние
let currentUser = localStorage.getItem('currentUser') || null;
let currentProgram = null;
let currentQuestionId = null;

// --- Управление отображением (SPA Навигация) ---
function showView(viewId) {
    document.querySelectorAll('.view-container').forEach(el => el.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');
    document.getElementById(viewId).style.display = 'flex';
    if(viewId === 'view-auth') {
        document.getElementById('view-app').style.display = 'none';
    } else {
        document.getElementById('view-auth').style.display = 'none';
    }
}

function showSection(sectionId) {
    document.querySelectorAll('.section-block').forEach(el => el.style.display = 'none');
    document.getElementById(sectionId).style.display = 'block';
}

// --- Авторизация ---
document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value.trim();
    if (username) {
        currentUser = username;
        localStorage.setItem('currentUser', currentUser);
        document.getElementById('current-username').textContent = currentUser;
        renderSubjects();
        showView('view-app');
        showSection('menu-section');
    }
});

document.getElementById('btn-logout').addEventListener('click', function() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    showView('view-auth');
});

// Проверка при загрузке
window.addEventListener('DOMContentLoaded', () => {
    if (currentUser) {
        document.getElementById('current-username').textContent = currentUser;
        renderSubjects();
        showView('view-app');
        showSection('menu-section');
    }
});

// --- Рендер Меню Предметов ---
function renderSubjects() {
    const container = document.getElementById('subjects-container');
    container.innerHTML = '';

    for (const [subject, programs] of Object.entries(subjectsData)) {
        const subjectDiv = document.createElement('div');
        subjectDiv.className = 'subject-item';

        const headerDiv = document.createElement('div');
        headerDiv.className = 'subject-header';
        headerDiv.textContent = subject;

        const programsDiv = document.createElement('div');
        programsDiv.className = 'programs-list';

        programs.forEach(prog => {
            const progDiv = document.createElement('div');
            progDiv.className = 'program-item';
            progDiv.textContent = prog;
            progDiv.onclick = () => openProgram(subject, prog);
            programsDiv.appendChild(progDiv);
        });

        headerDiv.onclick = () => {
            const isVisible = programsDiv.style.display === 'block';
            document.querySelectorAll('.programs-list').forEach(el => el.style.display = 'none'); // Закрыть другие
            programsDiv.style.display = isVisible ? 'none' : 'block';
        };

        subjectDiv.appendChild(headerDiv);
        subjectDiv.appendChild(programsDiv);
        container.appendChild(subjectDiv);
    }
}

// --- Открытие программы и рендер вопросов ---
function openProgram(subject, program) {
    currentProgram = { subject, program };
    document.getElementById('current-program-title').textContent = program;
    document.getElementById('add-question-form').style.display = 'none';
    renderQuestions();
    showSection('questions-section');
}

function renderQuestions() {
    const questions = JSON.parse(localStorage.getItem('questions')) || [];
    const filtered = questions.filter(q => q.program === currentProgram.program);
    const container = document.getElementById('questions-list');
    container.innerHTML = '';

    if (filtered.length === 0) {
        container.innerHTML = '<p style="color: #bbb;">Пока нет вопросов. Будьте первым!</p>';
        return;
    }

    filtered.forEach(q => {
        const card = document.createElement('div');
        card.className = 'card question-card';
        card.onclick = () => openQuestion(q.id);
        card.innerHTML = `
            <div class="q-title">${q.title}</div>
            <div>${q.text.length > 100 ? q.text.substring(0, 100) + '...' : q.text}</div>
            <div class="q-meta">
                <span>Автор: ${q.author} | ${q.date}</span>
                <span>Ответов: ${q.answers.length}</span>
            </div>
        `;
        container.appendChild(card);
    });
}

// --- Добавление вопроса ---
document.getElementById('btn-show-add-question').addEventListener('click', () => {
    document.getElementById('add-question-form').style.display = 'block';
});

document.getElementById('btn-submit-question').addEventListener('click', () => {
    const title = document.getElementById('new-q-title').value.trim();
    const text = document.getElementById('new-q-text').value.trim();
    if (!title || !text) return alert('Заполните все поля!');

    const questions = JSON.parse(localStorage.getItem('questions')) || [];
    const newQuestion = {
        id: Date.now(),
        subject: currentProgram.subject,
        program: currentProgram.program,
        title: title,
        text: text,
        author: currentUser,
        date: new Date().toLocaleDateString(),
        answers: []
    };
    
    questions.push(newQuestion);
    localStorage.setItem('questions', JSON.stringify(questions));
    
    document.getElementById('new-q-title').value = '';
    document.getElementById('new-q-text').value = '';
    document.getElementById('add-question-form').style.display = 'none';
    
    renderQuestions();
});

// --- Открытие страницы конкретного вопроса ---
function openQuestion(id) {
    currentQuestionId = id;
    const questions = JSON.parse(localStorage.getItem('questions')) || [];
    const q = questions.find(x => x.id === id);
    if(!q) return;

    document.getElementById('question-detail-card').innerHTML = `
        <h2 style="color: #ffbf00; border: none; padding: 0;">${q.title}</h2>
        <p style="white-space: pre-wrap; font-size: 1.1rem;">${q.text}</p>
        <div class="q-meta" style="margin-top: 20px;">
            <span>Спросил: ${q.author}</span>
            <span>${q.date}</span>
        </div>
    `;

    renderAnswers(q.answers);
    showSection('detail-section');
}

function renderAnswers(answers) {
    document.getElementById('answers-count').textContent = answers.length;
    const container = document.getElementById('answers-list');
    container.innerHTML = '';

    if (answers.length === 0) {
        container.innerHTML = '<p style="color: #bbb; margin-bottom: 20px;">Ответов пока нет.</p>';
        return;
    }

    answers.forEach(a => {
        const card = document.createElement('div');
        card.className = 'card answer-card';
        let imgHtml = a.file ? `<img src="${a.file}" class="answer-img" alt="Прикрепленный файл">` : '';
        
        card.innerHTML = `
            <div class="answer-text" style="white-space: pre-wrap;">${a.text}</div>
            ${imgHtml}
            <div class="q-meta">
                <span>Ответил: ${a.author}</span>
                <span>${a.date}</span>
            </div>
        `;
        container.appendChild(card);
    });
}

// --- Добавление ответа ---
document.getElementById('btn-submit-answer').addEventListener('click', () => {
    const text = document.getElementById('new-a-text').value.trim();
    const fileInput = document.getElementById('new-a-file');
    
    if (!text && fileInput.files.length === 0) return alert('Напишите текст или прикрепите фото!');

    const processAnswer = (fileData) => {
        const questions = JSON.parse(localStorage.getItem('questions')) || [];
        const qIndex = questions.findIndex(x => x.id === currentQuestionId);
        
        questions[qIndex].answers.push({
            text: text,
            file: fileData,
            author: currentUser,
            date: new Date().toLocaleDateString()
        });
        
        localStorage.setItem('questions', JSON.stringify(questions));
        
        document.getElementById('new-a-text').value = '';
        fileInput.value = '';
        renderAnswers(questions[qIndex].answers);
    };

    if (fileInput.files.length > 0) {
        const reader = new FileReader();
        reader.onload = function(e) {
            processAnswer(e.target.result); // Base64 string картинки
        };
        reader.readAsDataURL(fileInput.files[0]);
    } else {
        processAnswer(null);
    }
});