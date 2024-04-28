function fetchInfo() {
    const query = document.getElementById("queryInput").value;
    const payload = { link: query };

    const existingTable = document.querySelector("table");
        if (existingTable) {
            existingTable.remove();
        }
    const existingError = document.querySelector("p");
        if (existingError) {
            existingError.remove();
        }



    // Display "Loading" message
    const loadingMessage = document.createElement("p");
    loadingMessage.textContent = "Loading...";
    document.body.appendChild(loadingMessage);

    fetch(`/api/getInfo`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Clear existing table if it exists
            if (data.error) {
                const errorMessage = document.createElement("p");
                errorMessage.textContent = "Please check your link and try again";
                document.body.appendChild(errorMessage);
            } else {
                

                // Create table element
                const table = document.createElement("table");

                // Create table data rows
                Object.entries(data).forEach(([key, value]) => {
                    const row = document.createElement("tr");

                    // Create table data cell for index
                    const indexCell = document.createElement("td");
                    indexCell.innerHTML = `<strong>${key}</strong>`;
                    row.appendChild(indexCell);

                    // Create table data cell for data
                    const dataCell = document.createElement("td");
                    dataCell.textContent = value;
                    row.appendChild(dataCell);

                    table.appendChild(row);
                });

                // Remove "Loading" message
                document.body.removeChild(loadingMessage);

                // Append table to the body
                document.body.appendChild(table);
            }
        
            

            // Remove "Loading" message
            document.body.removeChild(loadingMessage);

            // Append table to the body
            document.body.appendChild(table);
        
        })
        .catch(error => {
            // Handle any errors here
            console.error('Error:', error);
            document.body.removeChild(loadingMessage);
        });
}