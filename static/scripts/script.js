let slideIndex = 1;
showSlides(slideIndex);
function plusSlides(n) {
    showSlides(slideIndex += n);
}
function currentSlide(n) {
    showSlides(slideIndex = n);
}
function showSlides(n) {
let i;
const slides = document.getElementsByClassName("mySlides");
const dots = document.getElementsByClassName("dot");
if (n > slides.length) {slideIndex = 1}    
if (n < 1) {slideIndex = slides.length}
for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
}
for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
}
slides[slideIndex-1].style.display = "block";  
    dots[slideIndex-1].className += " active";
}



// Sample plant data (replace with your actual data)
const plants = [
  {
    id: 1,
    name: "Snake Plant",
    image: ".static\images\plant.jpg",
    price: 19.99,
    description: "A low-maintenance indoor plant known for its air-purifying properties."
  },
  // ... more plant data
];

function createPlantItem(plant) {
  const item = document.createElement("div");
  item.classList.add("plant-item");

  const image = document.createElement("img");
  image.src = `images/${plant.image}`; // Assuming images folder
  item.appendChild(image);

  const title = document.createElement("h3");
  title.textContent = plant.name;
  item.appendChild(title);

  const price = document.createElement("p");
  price.textContent = `$${plant.price}`;
  item.appendChild(price);

  // Add to Cart button (replace with actual functionality)
  const addToCartButton = document.createElement("button");
  addToCartButton.textContent = "Add to Cart";
  addToCartButton.addEventListener("click", () => {
    // Add logic to handle adding plant to cart
    console.log(`Adding ${plant.name} to cart`);
  });
  item.appendChild(addToCartButton);

  // View button
  const viewButton = document.createElement("button");
  viewButton.textContent = "View";
  viewButton.addEventListener("click", () => {
    showPlantDescription(plant);
  });
  item.appendChild(viewButton);

  return item;
}

function showPlantDescription(plant) {
  const descriptionDiv = document.createElement("div");
  descriptionDiv.classList.add("plant-description");
  descriptionDiv.innerHTML = `<h3>${plant.name}</h3><p>${plant.description}</p>`;

  // Add functionality to close the description div (optional)
  const closeButton = document.createElement("button");
  closeButton.textContent = "Close";
  closeButton.addEventListener("click", () => {
    descriptionDiv.remove();
  });
  descriptionDiv.appendChild(closeButton);

  document.body.appendChild(descriptionDiv);
}

// Populate plant grid with plant items
plants.forEach((plant) => {
  const plantItem = createPlantItem(plant);
  document.querySelector(".plant-grid").appendChild(plantItem);
});
