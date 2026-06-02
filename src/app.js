document.addEventListener("DOMContentLoaded", () => {
  const modalContainer = document.getElementById("modal-container");
  if (!modalContainer) return; // Not on a post detail page

  const modalCloseBtn = document.getElementById("modal-close-btn");
  const modalTitle = document.getElementById("modal-title");
  const modalMediaContainer = document.getElementById("modal-media-container");
  const post = window.__POST_DATA__;
  if (!post || !post.assets) return;

  // Bind gallery clicks
  document.querySelectorAll(".gallery-item").forEach(galleryItem => {
    galleryItem.addEventListener("click", () => {
      const idx = parseInt(galleryItem.getAttribute("data-idx"));
      const asset = post.assets[idx];
      if (asset) {
        openModal(asset, post.assetsType);
      }
    });
  });

  // Modal Details
  function openModal(asset, type) {
    modalTitle.textContent = asset.title;

    // The asset.url has already been adjusted by build.py (e.g. '../gallery/sticker_1.png')
    const assetUrl = asset.url;

    if (type === "video") {
      modalMediaContainer.innerHTML = `<video src="${assetUrl}" autoplay loop muted playsinline controls style="max-height:320px; width:100%; object-fit:contain;"></video>`;
    } else {
      modalMediaContainer.innerHTML = `<img src="${assetUrl}" alt="${asset.title}" style="max-height:320px; width:100%; object-fit:contain;">`;
    }

    modalContainer.style.display = "flex";
  }

  modalCloseBtn.addEventListener("click", () => {
    modalContainer.style.display = "none";
    modalMediaContainer.innerHTML = "";
  });

  modalContainer.addEventListener("click", () => {
    modalContainer.style.display = "none";
    modalMediaContainer.innerHTML = "";
  });

  modalContainer.querySelector(".modal-content").addEventListener("click", (e) => {
    e.stopPropagation();
  });

});
