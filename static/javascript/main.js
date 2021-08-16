const searchField = document.querySelector("#searchField");
const whenNoFilms = document.querySelector('#when-no-films');
const tableOutput = document.querySelector("#replaceable-content")
tableOutput.style.display = 'none';
const tbody = document.querySelector(".t-body-output")

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        console.log('searchValue', searchValue);
        tbody.innerHTML = ""
        fetch("", {
            body: JSON.stringify({searchText: searchValue}),
            method: 'POST',
        })
            .then((res) => res.json())
            .then((data) => {
                console.log('data', data)
                if (data.length === 0) {
                    whenNoFilms.style.display = 'block';
                    tableOutput.style.display = 'none';
                } else {
                    whenNoFilms.style.display = 'none';
                    tableOutput.style.display = 'block';
                    data.forEach(item => {
                        tbody.innerHTML += `
                <tr>
                <td><a href="${item.link}">${item.name}</a></td>
                </tr>
                `
                    });
                }
            });
    } else {
        whenNoFilms.style.display = 'block';
        tableOutput.style.display = 'none';
    }

})
