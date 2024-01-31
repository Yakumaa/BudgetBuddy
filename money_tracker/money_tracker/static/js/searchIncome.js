const search = document.querySelector('#searchField');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const paginationContainer = document.querySelector('.pagination-container');
tableOutput.style.display = 'none';
const tableBody = document.querySelector('.table-body');
const noResults = document.querySelector('.no-results');


search.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    
    if (searchValue.trim().length > 0){
        paginationContainer.style.display = 'none';
        tableBody.innerHTML = "";
        fetch('/income/search-income', {
            body: JSON.stringify({ searchText: searchValue }),
            method: 'POST',
        })
        .then((res) => res.json())
        .then((data) => {
            console.log('data', data);
            appTable.style.display = 'none';
            tableOutput.style.display = 'block';

            if (data.length===0){
              noResults.style.display = 'block';
              tableOutput.style.display = 'none';
            }
            else{
              noResults.style.display = 'none';
              data.forEach((item) => {
                tableBody.innerHTML += `
                  <tr>
                    <td>${item.amount}</td>
                    <td>${item.description}</td>
                    <td>${item.source}</td>
                    <td>${item.date}</td>
                  </tr>
                `;
              });
            }
        });
    }
    else{
        appTable.style.display = 'block';
        tableOutput.style.display = 'none';
        paginationContainer.style.display = 'block';
    }
});
