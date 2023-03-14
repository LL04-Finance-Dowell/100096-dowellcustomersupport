const loginForm = document.getElementById("login-form");

fetch("https://100096.pythonanywhere.com/product_list/login", {
    method: "POST",
    body: JSON.stringify(),
    headers: {
      "Content-Type": "application/json"
    }
  })
  .then((response) => response.json())
  .then((data) => {
    console.log(data)
    // Display the data on the UI
    const productListDiv = document.getElementById("product-list");
    let html = "";
    for (const product of data) {
      html += `<div>${product.name}</div>`;
    }
    productListDiv.innerHTML = html;
  })
  .catch((error) => console.error(error));

