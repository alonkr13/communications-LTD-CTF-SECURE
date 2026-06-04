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

// Reverse of html.escape(quote=True). &amp; is decoded LAST so that an
// encoded literal like "&amp;lt;" becomes "&lt;", not "<".
const decodeHtml = (str) =>
  str
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&quot;", '"')
    .replaceAll("&#x27;", "'")
    .replaceAll("&amp;", "&");

// Render Functions
const renderCustomerRow = (packageId, customerName) => {
  const pkg = packageMap[packageId];
  const customerRow = document.createElement("span");
  customerRow.setAttribute("class","client-row");
  customerRow.setAttribute("data-customer",customerName);
  
  const p1 = document.createElement("p");
  const p2 = document.createElement("p");
  const p3 = document.createElement("p");
  const b = document.createElement("button");
  p1.textContent = decodeHtml(customerName);
  p2.textContent = pkg ? pkg[1] : "Unknown";
  p3.textContent = pkg ? `$${Number(pkg[4]).toFixed(2)}` : "-";
  b.setAttribute("class","delete-btn");
  b.setAttribute("data-customer",customerName);
  b.textContent = "Delete";
  
  customerRow.appendChild(p1);
  customerRow.appendChild(p2);
  customerRow.appendChild(p3);
  customerRow.appendChild(b);

  container.appendChild(customerRow);
  attachDeleteListener(b, customerRow);
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
const handleDelete = async (customerName, customerRow) => {
  const result = await DeleteCustomerRequest(customerName);

  if (result.message.includes("successfully")) {
    customers = customers.filter(([_, name]) => name !== customerName);
    sessionStorage.setItem("customers", JSON.stringify(customers));

    customerRow.remove();
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
    const storedName = result.customer_name;
    if (!storedName) {
      alert("Error: unexpected server response");
      return;
    }
    customers.push([packageId, storedName]);
    sessionStorage.setItem("customers", JSON.stringify(customers));
    renderCustomerRow(packageId, storedName);
    customerForm.reset();
    modal.classList.remove("active");
  } else {
    alert("Error: " + result.message);
  }
};

const attachDeleteListener = (btn, customerRow) => {
  btn.addEventListener("click", (e) => {
    const customerName = e.target.getAttribute("data-customer");
    if (confirm(`Are you sure you want to delete ${decodeHtml(customerName)}?`)) {
      handleDelete(customerName, customerRow);
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
