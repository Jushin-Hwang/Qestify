// 1. 필요한 모든 HTML 요소들을 선택합니다.
const sections = document.querySelectorAll('.question-section');
const progressBar = document.querySelector('.progress-bar');
const prevBtns = document.querySelectorAll('.prev-btn');
const nextBtns = document.querySelectorAll('.next-btn');
const submitBtn = document.querySelector('.submit-btn');


// 2. 전체 질문 개수와 현재 질문 인덱스, 답변을 저장할 객체를 설정합니다.
const totalQuestions = sections.length;
let currentQuestionIndex = 0;
const answers = {};

// 3. 특정 질문으로 화면을 부드럽게 이동하고 진행 바를 업데이트하는 함수입니다.
const navigateToQuestion = (index) => {
    sections[index].scrollIntoView({ behavior: 'smooth' });
    
    // 진행 바 너비 업데이트
    const progress = ((index + 1) / totalQuestions) * 100;
    progressBar.style.width = `${progress}%`;
    currentQuestionIndex = index;
};

// 4. 현재 질문의 답변을 answers 객체에 저장하는 함수입니다.
const saveAnswer = () => {
    const currentSection = sections[currentQuestionIndex];
    const questionKey = currentSection.dataset.question;

    // 질문 유형에 따라 답변을 저장합니다.
    const textInput = currentSection.querySelector('.text-input');
    if (textInput) {
        answers[questionKey] = textInput.value;
    }
};

// 5. 현재 질문에 대한 유효성을 검사하는 함수입니다.
const validateCurrentAnswer = () => {
    const currentSection = sections[currentQuestionIndex];
    const questionKey = currentSection.dataset.question;
    const answer = answers[questionKey];

    // 값이 없거나(undefined, null, 빈 문자열), false인 경우 (체크박스)
    if (answer === undefined || answer === null || answer === '' || answer === false) {
        alert('필수 항목을 입력하거나 선택해주세요!');
        return false;
    }

    return true;
};


// --- 이벤트 리스너 설정 ---

// 6. '다음' 버튼들에 클릭 이벤트를 추가합니다.
nextBtns.forEach(button => {
    button.addEventListener('click', () => {
        saveAnswer();
        if (validateCurrentAnswer()) {
            if (currentQuestionIndex < totalQuestions - 1) {
                navigateToQuestion(currentQuestionIndex + 1);
            }
        }
    });
});

// 7. '이전' 버튼들에 클릭 이벤트를 추가합니다.
prevBtns.forEach(button => {
    button.addEventListener('click', () => {
        if (currentQuestionIndex > 0) {
            navigateToQuestion(currentQuestionIndex - 1);
        }
    });
});

// 9. '제출하기' 버튼에 서버 전송 이벤트를 추가합니다.
submitBtn.addEventListener('click', async () => {
    saveAnswer();
    if (!validateCurrentAnswer()) return;

    // 1. FormData 객체를 생성합니다.
    const formData = new FormData();

    // 2. 텍스트 데이터를 FormData에 추가합니다.
    formData.append('name', answers.user_name);
    formData.append('answers', answers.user_answer); // answers 객체는 JSON 문자열로 변환

    try {
        // 4. fetch 요청을 보냅니다.
        // ⚠️ 중요: FormData를 보낼 때는 headers의 'Content-Type'을 제거해야 합니다.
        // 브라우저가 자동으로 'multipart/form-data'로 설정해줍니다.
        const response = await fetch('http://35.238.93.210:5000/api/submit', {
            method: 'POST',
            body: formData, // JSON.stringify 대신 formData 객체를 그대로 전달
        });

        const result = await response.json();

        if (result.success) {
            const lastSection = document.querySelector('[data-question="thank_you"]');
            if (lastSection) {
                 lastSection.scrollIntoView({ behavior: 'smooth' });
            } else {
                 alert('신청서가 성공적으로 제출되었습니다!');
            }
        } else {
            alert(`제출 실패: ${result.message}`);
        }
    } catch (error) {
        console.error('제출 중 오류 발생:', error);
        alert('서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.');
    }
});