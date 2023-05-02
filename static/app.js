
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
    document.getElementById('discover-art').style.display = 'none';


    fetch('/next_artwork')
        .then(response => response.json())
        .then(painting => {
            updateArtwork(painting);
            document.getElementById('discover-art').style.display = 'block';
            showArt();
        })
        .catch(error => {
            console.error('Error fetching artwork:', error);
            document.getElementById('discover-art').style.display = 'block';
        });
}

document.getElementById('discover-art').addEventListener('click', function() {
    getNextArtwork();
});

document.getElementById('discover-another').addEventListener('click', function() {
    getNextArtwork();
});
