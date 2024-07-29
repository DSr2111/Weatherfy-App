document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("city-search");
  const suggestions = document.getElementById("suggestions");

  // setting up Refresh and Delete buttons to work on Dashboard
  setupDeleteButtons();
  setupRefreshButtons();

  function setupDeleteButtons() {
    document.querySelectorAll(".delete-favorite").forEach((button) => {
      button.addEventListener("click", function () {
        const cityName = button.getAttribute("data-city");
        deleteFavorite(cityName);
      });
    });
  }

  function setupRefreshButtons() {
    document.querySelectorAll(".refresh-weather").forEach((button) => {
      button.addEventListener("click", function () {
        const cityName = button.getAttribute("data-city");
        const lat = button.getAttribute("data-lat");
        const lon = button.getAttribute("data-lon");
        fetchWeatherForDashboard(cityName, lat, lon);
      });
    });
  }

  // Drop down list in search bar as user types
  searchInput.addEventListener("input", function () {
    const query = searchInput.value;
    suggestions.innerHTML = "";

    if (query) {
      fetch(`/get_suggestions?query=${query}`)
        .then((response) => response.json())
        .then((data) => {
          if (data.length > 0) {
            suggestions.style.display = "block";
            data.forEach((city) => {
              const suggestionItem = document.createElement("a");
              suggestionItem.classList.add(
                "list-group-item",
                "list-group-item-action"
              );
              suggestionItem.textContent = `${city.name}, ${city.state}, ${city.country}`;
              suggestionItem.addEventListener("click", function () {
                searchInput.value = city.name;
                suggestions.innerHTML = "";
                suggestions.style.display = "none";
                fetchWeather(city.lat, city.lon, city.name);
              });
              suggestions.appendChild(suggestionItem);
            });
          } else {
            suggestions.style.display = "none";
          }
        })
        .catch((error) =>
          console.error("Error fetching city suggestions:", error)
        );
    } else {
      suggestions.style.display = "none";
    }
  });

  document
    .getElementById("search-button")
    .addEventListener("click", function () {
      const cityName = searchInput.value;
      if (cityName) {
        fetch(`/get_weather?city_name=${cityName}`)
          .then((response) => response.json())
          .then((data) => {
            displayWeather(data);
          })
          .catch((error) =>
            console.error("Error fetching weather data:", error)
          );
      }
    });

  function fetchWeather(lat, lon, name) {
    fetch(`/get_weather?lat=${lat}&lon=${lon}&city_name=${name}`)
      .then((response) => response.json())
      .then((data) => {
        displayWeather(data);
      })
      .catch((error) => console.error("Error fetching weather data:", error));
  }

  // Logic to show weather data as a card, once city is selected
  function displayWeather(data) {
    const weatherDataDiv = document.getElementById("weather-data");
    if (data.error) {
      weatherDataDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
    } else {
      weatherDataDiv.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h3 class="card-title">Weather in ${data.name}</h3>
                        <p class="card-text" id="temp-${data.name}">Temperature: ${data.temp} °C</p>
                        <p class="card-text" id="desc-${data.name}">Weather: ${data.description}</p>
                        <p class="card-text" id="lat-${data.lat}">Latitude: ${data.lat}</p>
                        <p class="card-text" id="lon-${data.lon}">Longitude: ${data.lon}</p>
                        <img src="http://openweathermap.org/img/wn/${data.icon}.png" alt="Weather Icon">
                        <button class="btn btn-outline-danger favorite-button" data-city="${data.name}" data-lat="${data.lat}" data-lon="${data.lon}">
                            <i class="fa fa-heart"></i>
                        </button>
                    </div>
                </div>
            `;
      const favoriteButton = weatherDataDiv.querySelector(".favorite-button");
      favoriteButton.addEventListener("click", function () {
        favoriteCity(data.name, data.lat, data.lon);
      });
    }
    setupDeleteButtons(); // Ensure delete buttons are set up after displaying weather
    setupRefreshButtons(); // Ensure refresh buttons are set up after displaying weather
  }

  // Favoriting a city in Search results
  function favoriteCity(cityName, lat, lon) {
    fetch("/favorite", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ city_name: cityName, lat: lat, lon: lon }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          alert(`${cityName} has been added to your favorites!`);
        } else {
          alert("Error adding favorite.");
        }
      })
      .catch((error) => console.error("Error favoriting city:", error));
  }

  // Deleting a favorited city from dashboard
  function deleteFavorite(cityName) {
    fetch("/delete_favorite", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ city_name: cityName }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        if (data.status === "success") {
          alert(`${cityName} has been removed from your favorites.`);
          const favoriteCard = document.querySelector(
            `.favorite-card[data-city="${cityName}"]`
          );
          if (favoriteCard) {
            favoriteCard.remove();
          }
        } else {
          alert(`Error removing favorite: ${data.message}`);
        }
      })
      .catch((error) => console.error("Error removing favorite:", error));
  }

  // Refresh weather data logic
  function fetchWeatherForDashboard(cityName, lat, lon) {
    fetch(`/get_weather?city_name=${cityName}&lat=${lat}&lon=${lon}`)
      .then((response) => response.json())
      .then((data) => {
        if (!data.error) {
          document.getElementById(
            `temp-${data.name}`
          ).textContent = `Temperature: ${data.temp} °C`;
          document.getElementById(
            `desc-${data.name}`
          ).textContent = `Weather: ${data.description}`;
          document.getElementById(
            `icon-${data.name}`
          ).src = `http://openweathermap.org/img/wn/${data.icon}.png`;
        }
      })
      .catch((error) => console.error("Error fetching weather data:", error));
  }

  setTimeout(function () {
    const flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach((message) => (message.style.display = "none"));
  }, 1500);
});
