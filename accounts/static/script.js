let currentQuestionNumber = 1;
let totalQuestions = 0;
let answeredQuestions = new Map();
let reviewQuestions = new Set();

document.addEventListener("DOMContentLoaded", function() {
    fetch(`${window.location.origin}/accounts/api/total-questions/`)
        .then(res => res.json())
        .then(data => {
            totalQuestions = data.total;
            console.log("Point 1:Total Questions:  ", totalQuestions);
            generateQuestionGrid(totalQuestions);
            loadQuestion(currentQuestionNumber);
        });
    document.getElementById("question-form").addEventListener("submit", function(e) {
        e.preventDefault();
        saveAnswer();
        alert("Answer saved successfully!");
    });
});


function generateQuestionGrid(totalQuestions) {
    const grid = document.getElementById('quant-grid'); // or 'verbal-grid'
    grid.innerHTML = ''; // Clear previous

    for (let i = 1; i <= totalQuestions; i++) {
        const btn = document.createElement('button');
        btn.id = `q${i}`;
        btn.textContent = i;
        btn.className = 'badge m-1 border';
        btn.onclick = () => loadQuestion(i);
        grid.appendChild(btn);
    }

    // Now safe to update first question’s status
    updateGridStatus(1, 'bg-primary');
}

function loadQuestion(number) {
    fetch(`${window.location.origin}/accounts/api/get_question/${number}/`)
        .then(res => res.json())
        .then(data => {
            currentQuestionNumber = number; // UI sequence
            currentQuestionId = data.id; // actual DB ID

            document.getElementById('question-number').textContent = number;
            document.getElementById('question-text').textContent = data.text;

            const optionsContainer = document.getElementById('options-container');
            optionsContainer.innerHTML = '';

            data.options.forEach(option => {
                const optionHTML = `
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="answer" id="opt-${option.id}" value="${option.id}">
                        <label class="form-check-label" for="opt-${option.id}">${option.text}</label>
                    </div>`;
                optionsContainer.innerHTML += optionHTML;
            });

            if (answeredQuestions.has(data.id)) {
                const selectedId = answeredQuestions.get(data.id);
                const input = document.getElementById(`opt-${selectedId}`);
                if (input) input.checked = true;
            }

            updateGridStatus(number, data.id, 'bg-primary'); // current question highlight
        });
}

function saveAnswer() {
    const selectedOption = document.querySelector('input[name="answer"]:checked');
    if (!selectedOption || !currentQuestionId) return Promise.resolve();

    const selectedOptionId = selectedOption.value;

    return fetch(`${window.location.origin}/accounts/api/save_answer/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            question_id: currentQuestionId,
            selected_option_id: selectedOptionId
        })
    }).then(response => {
        if (response.ok) {
            answeredQuestions.set(currentQuestionId, selectedOptionId);
            updateGridStatus(currentQuestionNumber, currentQuestionId);
        }
    });
}

async function loadNext() {
    await saveAnswer(); // ⏳ wait for answer to be saved and UI to update
    if (currentQuestionNumber < totalQuestions) {
        console.log("Point 4: Loading next question" + (currentQuestionNumber));
        currentQuestionNumber++;
        loadQuestion(currentQuestionNumber);
    }
}

async function loadPrevious() {
    await saveAnswer();
    if (currentQuestionNumber > 1) {
        currentQuestionNumber--;
        loadQuestion(currentQuestionNumber);
    }
}

function markForReview() {
    reviewQuestions.add(currentQuestionNumber);
    updateGridStatus(currentQuestionNumber);
}

function updateGridStatus(questionNumber, questionId, statusClass = '') {
    const button = document.getElementById(`q${questionNumber}`);
    if (!button) {
        console.warn(`No button found for question ${questionNumber}`);
        return;
    }

    // Reset base classes
    button.className = 'badge m-1 border';

    // Apply status based on questionId
    if (answeredQuestions.has(questionId)) {
        button.classList.add('bg-success');
    } else if (reviewQuestions.has(questionId)) {
        button.classList.add('bg-warning');
    } else if (statusClass) {
        button.classList.add(statusClass); // Highlight current
    }
}


function getCSRFToken() {
    let csrftoken = null;
    const cookies = document.cookie.split('; ');
    for (let row of cookies) {
        row = row.trim();
        if (row.startsWith('csrftoken=')) {
            csrftoken = row.split('=')[1];
            break;
        }
    }
    return csrftoken || '';
}