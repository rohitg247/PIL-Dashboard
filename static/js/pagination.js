const itemsPerPage = 10;
const reportData = document.getElementById('reportData').getElementsByTagName('tr');
const totalPages = Math.ceil(reportData.length / itemsPerPage);
let currentPage = 1;

function showPage(pageNumber) {
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, reportData.length);

    for (let i = 0; i < reportData.length; i++) {
        if (i >= startIndex && i < endIndex) {
            reportData[i].style.display = 'table-row';
        } else {
            reportData[i].style.display = 'none';
        }
    }
}

function updatePagination() {
    const paginationContainer = document.querySelector('.pagination');
    paginationContainer.innerHTML = '';

    const prevButton = document.createElement('li');
    prevButton.classList.add('page-item');
    if (currentPage === 1) {
        prevButton.classList.add('disabled');
    }
    prevButton.innerHTML = `
        <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Previous</a>
    `;
    prevButton.addEventListener('click', function (event) {
        event.preventDefault();
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
            updatePagination();
        }
    });
    paginationContainer.appendChild(prevButton);

    const totalPagesToShow = 5;
    let startPage = Math.max(1, currentPage - Math.floor(totalPagesToShow / 2));
    let endPage = Math.min(totalPages, startPage + totalPagesToShow - 1);
    if (endPage - startPage + 1 < totalPagesToShow) {
        startPage = Math.max(1, endPage - totalPagesToShow + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
        const pageButton = document.createElement('li');
        pageButton.classList.add('page-item');
        if (i === currentPage) {
            pageButton.classList.add('active');
            pageButton.setAttribute('aria-current', 'page');
        }
        pageButton.innerHTML = `
            <a class="page-link" href="#">${i}</a>
        `;
        pageButton.addEventListener('click', function (event) {
            event.preventDefault();
            currentPage = i;
            showPage(currentPage);
            updatePagination();
        });
        paginationContainer.appendChild(pageButton);
    }

    const nextButton = document.createElement('li');
    nextButton.classList.add('page-item');
    if (currentPage === totalPages) {
        nextButton.classList.add('disabled');
    }
    nextButton.innerHTML = `
        <a class="page-link" href="#">Next</a>
    `;
    nextButton.addEventListener('click', function (event) {
        event.preventDefault();
        if (currentPage < totalPages) {
            currentPage++;
            showPage(currentPage);
            updatePagination();
        }
    });
    paginationContainer.appendChild(nextButton);
}

showPage(currentPage);
updatePagination();
