function showLoader() {
    document.getElementById('discover-art').style.display = 'none';
    document.getElementById('loader').style.display = 'block';
}

function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}

function showArt() {
    document.getElementById('art-info').style.display = 'block';
    document.getElementById('painting-img').style.display = 'block';
}

function updateArtwork(painting) {
    document.getElementById('art-name').innerHTML = painting.title;
    document.getElementById('art-name').style.display = 'block';
    document.getElementById('art-desc').innerHTML = painting.info;
    document.getElementById('painting-img').src = painting.image_url;
    document.getElementById('painting-img').alt = painting.title;
    document.getElementById('discover-another').style.display = 'block';
}

function getNextArtwork() {
    showLoader();

    fetch('/next_artwork')
        .then(response => response.json())
        .then(painting => {
            updateArtwork(painting);
            hideLoader();
            showArt();
        })
        .catch(error => {
            console.error('Error fetching artwork:', error);
            hideLoader();
        });
}

document.getElementById('discover-art').addEventListener('click', function() {
    getNextArtwork();
});

document.getElementById('discover-another').addEventListener('click', function() {
    getNextArtwork();
});
