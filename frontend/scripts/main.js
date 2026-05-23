import { LoginRequest } from "./requests.js";
import { arrayOfCustomers, arrayOfPackages } from "./global-data.js";

const loginButton = document.querySelector("#login-button");
const userInput = document.querySelector("#user-input");
const passwordInput = document.querySelector("#password-input");

loginButton.addEventListener("click", async (event) => {
  event.preventDefault();

  const user = userInput.value;
  const pass = passwordInput.value;

  const result = await LoginRequest({ username: user, password: pass });

  if (!result || !result.data) {
    alert(result?.message || "Login failed. Please try again.");
    return;
  }

  arrayOfPackages.push(result.data.packages);
  arrayOfCustomers.push(result.data.customers);

  /* Using sessionStorage to store customer and package data,
      if not data will be lost */
  sessionStorage.setItem("customers", JSON.stringify(result.data.customers));
  sessionStorage.setItem("packages", JSON.stringify(result.data.packages));
  window.location.href = "clients.html";
});
