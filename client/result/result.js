document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('app-table-body');
    const exportCsvBtn = document.getElementById('export-csv-btn');
    const modal = document.getElementById('detail-modal');
    const closeModalBtn = document.querySelector('.close-btn');
    const modalBody = document.getElementById('modal-body');
    let applicationsData = []; // 전체 데이터를 저장할 변수

    // 1. 서버에서 모든 신청서 데이터를 가져와서 표를 채웁니다.
    const loadApplications = async () => {
        try {
            const response = await fetch('http://35.238.93.210:5000/api/applications');
            applicationsData = await response.json();

            console.log(applicationsData);
            
            tableBody.innerHTML = ''; // 기존 내용을 비웁니다.

            applicationsData.forEach(app => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${app[2]}</td>
                `;
                // 각 행에 클릭 이벤트를 추가하여 모달을 엽니다.
                row.addEventListener('click', () => showDetail(app.id));
                tableBody.appendChild(row);
            });
        } catch (error) {
            console.error('데이터를 불러오는 중 오류 발생:', error);
            tableBody.innerHTML = `<tr><td colspan="4">데이터를 불러올 수 없습니다.</td></tr>`;
        }
    };

    // 2. 특정 ID의 상세 정보를 모달에 표시합니다.
    const showDetail = (id) => {
        const app = applicationsData.find(a => a.id === id);
        if (!app) return;

        let detailHtml = '';
        // 'answers' 객체의 모든 키와 값을 순회하며 HTML을 생성합니다.
        for (const [key, value] of Object.entries(app.answers)) {
            detailHtml += `<p><strong>${key}:</strong> ${value}</p>`;
        }
        
        // 이미지 URL이 있다면 이미지 태그를 추가합니다.
        if (app.image_url) {
            // GCP URL을 로컬 서버 URL로 변환해야 할 수 있습니다. 
            // 일단은 그대로 사용합니다.
            detailHtml += `<p><strong>fan_photo:</strong></p><img src="http://35.238.93.210:5000/${app.image_url}" alt="팬 인증 사진">`;
        }

        modalBody.innerHTML = detailHtml;
        modal.style.display = 'block';
    };

    // 4. 모달 닫기 이벤트
    closeModalBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    // 페이지가 로드되면 바로 데이터를 불러옵니다.
    loadApplications();
});