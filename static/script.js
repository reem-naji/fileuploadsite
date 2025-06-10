async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('status');

    if(!fileInput.files[0]){
        status.textContent = "Please select a file."
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    try{
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        if(result.success){
            status.textContent = "File uploaded! Download link: " + result.url;
            fetchFiles();
        }else {
            status.textContent = "Error: " + result.error;
        }
    } catch(error){
        status.textContent = "Upload failed" + error.message;
    }
    
}

async function fetchFiles() {
        const fileListDiv = document.getElementById('fileList');
        fileListDiv.innerHTML = '<h2>Uploaded Files</h2>';
        
        try{
            const response = await fetch('/files');

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const files = await response.json();

            if (files.error) {
                fileListDiv.innerHTML += `<p class="error">${files.error}</p>`;
                return;
            }

            if (files.length === 0) {
                fileListDiv.innerHTML += "<p>No files uploaded yet</p>";
                return;
            }

            files.forEach(file => {
                const fileElement = document.createElement('div');
                fileElement.innerHTML = `
                    <p>
                        <a href="${file.url}" target="_blank">${file.name}</a>
                        (${Math.round(file.size / 1024)} KB)
                    </p>
                `;
                fileListDiv.appendChild(fileElement);
            });

        } catch (error) {
        fileListDiv.innerHTML = `<p>Error loading files: ${error.message}</p>`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchFiles(); 
});