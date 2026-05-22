const baseURL = `${window.location.protocol}//${window.location.hostname}:8000`;

export const LoginRequest = async (data) => {
  try {
    const response = await fetch(`${baseURL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log("results are: ", result);
    return result.data;
  } catch (error) {
    console.error("Error:", error);
  }
};

export const ChangePasswordRequest = async (data) => {
  try {
    const response = await fetch(`${baseURL}/auth/change-password`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error:", error);
    return { message: "Failed to change password" };
  }
};

export const DeleteCustomerRequest = async (customerName) => {
  try {
    const response = await fetch(`${baseURL}/auth/delete-package/${customerName}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error:", error);
    return { message: "Error deleting customer" };
  }
};

export const CreateCustomerRequest = async (packageId, customerName) => {
  try {
    const response = await fetch(`${baseURL}/auth/create-customer`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        package_id: packageId,
        customer_name: customerName,
      }),
    });

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error:", error);
    return { message: "Error creating customer" };
  }
};