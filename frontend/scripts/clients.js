import { DeleteCustomerRequest, CreateCustomerRequest } from "./requests.js";

if (!sessionStorage.getItem("customers")) window.location.href = "login.html";

// DOM Elements
const container = document.querySelector(".clients-container");
const addCustomerBtn = document.getElementById("add-customer-btn");
const modal = document.getElementById("customer-modal");
const cancelBtn = document.getElementById("cancel-btn");
const modalOverlay = document.querySelector(".modal-overlay");
const customerForm = document.getElementById("customer-form");
const customerNameInput = document.getElementById("customer-name");
const packageSelect = document.getElementById("package-select");

// Data from SessionStorage
let customers = JSON.parse(sessionStorage.getItem("customers"));
const packages = JSON.parse(sessionStorage.getItem("packages"));
const packageMap = Object.fromEntries(packages.map((p) => [p[0], p]));

// Render Functions
const renderCustomerRow = (packageId, customerName) => {
  const pkg = packageMap[packageId];
  container.insertAdjacentHTML(
    "beforeend",
    `<span class="client-row" data-customer="${customerName}">
      <p>${customerName}</p>
      <p>${pkg ? pkg[1] : "Unknown"}</p>
      <p>${pkg ? `$${Number(pkg[4]).toFixed(2)}` : "-"}</p>
      <button class="delete-btn" data-customer="${customerName}">Delete</button>
    </span>`
  );
  attachDeleteListener(document.querySelector(`[data-customer="${customerName}"] .delete-btn`));
};

const renderPackageDropdown = () => {
  packages.forEach(([packageId, packageName, downloadSpeed, uploadSpeed]) => {
    const option = document.createElement("option");
    option.value = packageId;
    option.textContent = `${packageName} - ${downloadSpeed}/${uploadSpeed}`;
    packageSelect.appendChild(option);
  });
};

// Event Handlers
const handleDelete = async (customerName) => {
  const result = await DeleteCustomerRequest(customerName);

  if (result.message.includes("successfully")) {
    customers = customers.filter(([_, name]) => name !== customerName);
    sessionStorage.setItem("customers", JSON.stringify(customers));

    document.querySelector(`[data-customer="${customerName}"]`).remove();
  } else {
    alert("Error: " + result.message);
  }
};

const handleCreateCustomer = async (e) => {
  e.preventDefault();

  const customerName = customerNameInput.value.trim();
  const packageId = parseInt(packageSelect.value);

  if (!customerName || !packageId) {
    alert("Please fill in all fields");
    return;
  }

  const result = await CreateCustomerRequest(packageId, customerName);

  if (result.message.includes("successfully")) {
    customers.push([packageId, customerName]);
    sessionStorage.setItem("customers", JSON.stringify(customers));
    renderCustomerRow(packageId, customerName);
    customerForm.reset();
    modal.classList.remove("active");
  } else {
    alert("Error: " + result.message);
  }
};

const attachDeleteListener = (btn) => {
  btn.addEventListener("click", (e) => {
    const customerName = e.target.getAttribute("data-customer");
    if (confirm(`Are you sure you want to delete ${customerName}?`)) {
      handleDelete(customerName);
    }
  });
};

// Initialize
renderPackageDropdown();
customers.forEach(([packageId, customerName]) => {
  renderCustomerRow(packageId, customerName);
});

// Event Listeners
addCustomerBtn.addEventListener("click", () => {
  modal.classList.add("active");
});

cancelBtn.addEventListener("click", () => {
  modal.classList.remove("active");
});

modalOverlay.addEventListener("click", () => {
  modal.classList.remove("active");
});

customerForm.addEventListener("submit", handleCreateCustomer);
