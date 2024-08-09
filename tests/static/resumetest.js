async function fetchInfo() {
    const query = document.getElementById("queryInput").value;
    const payload = { link: query };
    const existingError = document.querySelector("p");
        if (existingError) {
            existingError.remove();
        }
    const loadingMessage = document.createElement("p");
    loadingMessage.textContent = "Loading...";
    document.body.appendChild(loadingMessage);
    
    var jsonData ={};

    await fetch('/api/getJobDescription', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        jsonData = data;
        // Clear existing table if it exists

        var pdfText = sessionStorage.getItem('pdfText');

        // Check if pdfText is not null or undefined
        if (pdfText) {
            // Do something with the retrieved PDF text, such as displaying it
            jsonData.resume_text = pdfText;
            console.log(jsonData);
            fetch('/api/compareResume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            }).then(response => response.json())
            .then(data => {
                // console.log(data);

                // Append the response as a paragraph to the HTML
                const existingError = document.querySelector("p");
                if (existingError) {
                    existingError.remove();
                }
                const responseParagraph = document.createElement('p');
                responseParagraph.innerHTML = data;
                document.body.appendChild(responseParagraph);


            })

        } else {
        // Handle the case where pdfText is not found in sessionStorage
        alert('Please upload a resume');

        }
    })
    .catch(error => {
        // Handle any errors here
        console.error('Error:', error);
    });

    

        
}


function printPdfText()
        {
            var pdfText = sessionStorage.getItem('pdfText');

            // Check if pdfText is not null or undefined
            if (pdfText) {
                // Do something with the retrieved PDF text, such as displaying it
                console.log(pdfText);
            } else {
            // Handle the case where pdfText is not found in sessionStorage
            console.log('PDF text not found in sessionStorage.');
            }
        }

        function uploadPdf() {
            var fileInput = document.getElementById('fileInput');
            var file = fileInput.files[0];

            if (!file) {
                alert('Please select a file');
                return;
            }

            var formData = new FormData();
            formData.append('file', file);

            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    // Store the text in sessionStorage
                    sessionStorage.setItem('pdfText', data.text);
                    alert('PDF text has been stored.');
                }
            })
            .catch(error => console.error('Error:', error));
        }





