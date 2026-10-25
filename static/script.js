
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("image");
    const area = document.getElementById("upload-area");
    const title = document.getElementById("upload-title");
    const subtitle = document.getElementById("upload-subtitle");
    const previewContainer = document.getElementById("preview-container");
    const previewImage = document.getElementById("preview-image");

    function showPreview(file) {
        if (!file) return;

        if (!file.type.startsWith("image/")) {
            alert("Please select a valid image file.");
            input.value = "";
            return;
        }

        title.textContent = file.name;
        subtitle.textContent = "Image selected successfully";

        const reader = new FileReader();

        reader.onload = (event) => {
            previewImage.src = event.target.result;
            previewContainer.hidden = false;
        };

        reader.readAsDataURL(file);
    }

    input.addEventListener("change", () => {
        showPreview(input.files[0]);
    });

    area.addEventListener("dragover", (event) => {
        event.preventDefault();
        area.classList.add("dragging");
    });

    area.addEventListener("dragleave", () => {
        area.classList.remove("dragging");
    });

    area.addEventListener("drop", (event) => {
        event.preventDefault();
        area.classList.remove("dragging");

        const file = event.dataTransfer.files[0];

        if (file) {
            const transfer = new DataTransfer();
            transfer.items.add(file);
            input.files = transfer.files;
            showPreview(file);
        }
    });

    const resetButton = document.createElement("button");
    resetButton.type = "button";
    resetButton.textContent = "Clear selected image";
    resetButton.className = "download-btn";
    resetButton.style.display = "none";

    previewContainer.after(resetButton);

    resetButton.addEventListener("click", () => {
        input.value = "";
        previewImage.src = "";
        previewContainer.hidden = true;
        resetButton.style.display = "none";
        title.textContent = "Drop your image here";
        subtitle.textContent = "or click to browse your files";
    });

    input.addEventListener("change", () => {
        resetButton.style.display = input.files.length ? "flex" : "none";
    });
});
