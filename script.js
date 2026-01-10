const input = document.getElementById("movieInput");
const button = document.getElementById("recommendBtn");
const cardsContainer = document.querySelector(".cards-container");

// Overlay elements
const overlay = document.getElementById("movieOverlay");
const closeOverlay = document.getElementById("closeOverlay");
const overlayTitle = document.getElementById("overlayTitle");
const overlayDescription = document.getElementById("overlayDescription");
const overlayPlayBtn = document.getElementById("overlayPlayBtn");
const overlayTrailer = document.getElementById("overlayTrailer");
const openYoutubeBtn = document.getElementById("openYoutubeBtn");

// ====================
// Recommend button
// ====================
button.addEventListener("click", async () => {
  const movie = input.value.trim();
  if (!movie) return;

  cardsContainer.innerHTML = "<p>Loading...</p>";

  try {
    const res = await fetch(
      `http://cinesense-ai-3.onrender.com/recommend?movie=${encodeURIComponent(movie)}`
    );

    const data = await res.json();

    if (!data.results || data.results.length === 0) {
      cardsContainer.innerHTML = "<p>No results found.</p>";
      return;
    }

    renderCards(data.results);
  } catch (err) {
    console.error(err);
    cardsContainer.innerHTML = "<p>Backend error</p>";
  }
});

// ====================
// Render cards
// ====================
function renderCards(movies) {
  cardsContainer.innerHTML = "";

  movies.forEach((movie) => {
    const card = document.createElement("div");
    card.className = "movie-card";

    // Store TMDB data on card
    card.dataset.title = movie.title;
    card.dataset.overview = movie.overview;
    card.dataset.backdrop = movie.backdrop;
    card.dataset.trailer = movie.trailer;

    card.innerHTML = `
      <div class="card-inner">
        <div class="card-front">
          <h3>${movie.title}</h3>
        </div>
      </div>
    `;

    cardsContainer.appendChild(card);
  });
}

// ====================
// Open overlay on card click
// ====================
document.addEventListener("click", (e) => {
  const card = e.target.closest(".movie-card");
  if (!card) return;

  const key = card.dataset.trailer;

  overlayTitle.innerText = card.dataset.title;
  overlayDescription.innerText =
    card.dataset.overview || "No description available.";

  const bg = card.dataset.backdrop || "fallback.jpg";

  overlay.style.backgroundImage =
    "linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.55)), url(" + bg + ")";


  // Reset trailer
  overlayTrailer.classList.add("hidden");
  overlayTrailer.src = "";

  // ▶ Play Trailer (best-effort embed)
  overlayPlayBtn.onclick = () => {
    if (!key) {
      alert("No trailer available for this movie");
      return;
    }

    overlayTrailer.classList.remove("hidden");
    overlayTrailer.src =
      "https://www.youtube-nocookie.com/embed/" +
      key +
      "?autoplay=1&mute=1&rel=0";

    overlayPlayBtn.style.display = "inline-block";

    overlayPlayBtn.style.display = "none";
  };

  // 🔗 Open on YouTube (always works)
  openYoutubeBtn.onclick = () => {
    if (!key) return;

    window.open(
      "https://www.youtube.com/watch?v=" + key,
      "_blank"
    );
  };

  overlay.classList.remove("hidden");
});

// ====================
// Close overlay
// ====================
closeOverlay.addEventListener("click", () => {
  overlay.classList.add("hidden");
  overlayTrailer.classList.add("hidden");
  overlayTrailer.src = "";

  overlayPlayBtn.style.display = "inline-block";
});
