document.addEventListener("DOMContentLoaded", () => {
    const loadButton = document.getElementById("load-button");
    const imageContainer = document.getElementById("image-container");
  
    loadButton.addEventListener("click", async () => {
      loadButton.disabled = true;
      const response = await fetch("/get_painting");
      const result = await response.json();
      if (result.success) {
        const { image_url, title, description } = result.data;
        document.querySelector("h1.title").textContent = title;
        document.querySelector("p.description").textContent = description;
        imageContainer.src = image_url;
      } else {
        alert("Failed to load painting, please try again.");
      }
      loadButton.disabled = false;
    });
  });
  