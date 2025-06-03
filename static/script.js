// This script runs after the DOM is fully loaded
window.addEventListener("DOMContentLoaded", () => {
  fetch("/contracts")
    .then(res => res.json())
    .then(contracts => {
      const container = document.getElementById("contracts");
      container.innerHTML = ""; // Clear the "Loading..." text

      if (contracts.length === 0) {
        container.textContent = "No contracts submitted yet.";
        return;
      }

      // Loop through each contract and create a display block
      contracts.forEach((contract, index) => {
        const div = document.createElement("div");
        div.className = "contract";

        div.innerHTML = `
          <p><strong>DAD:</strong> ${contract.dad}</p>
          <p>Status: ${contract.status}</p>
          ${contract.status === "submitted" ? `
            <form action="/complete" method="post">
              <input type="hidden" name="index" value="${index}">
              <button type="submit">Mark as Completed</button>
            </form>
          ` : ""}
          <hr>
        `;
        container.appendChild(div);
      });
    })
    .catch(err => {
      console.error("Error loading contracts:", err);
      const container = document.getElementById("contracts");
      container.textContent = "Failed to load contracts.";
    });
  document.getElementById("dad-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const data = new FormData(form);
  const response = await fetch("/submit", {
    method: "POST",
    body: new URLSearchParams(data),
  });

  if (response.status === 400) {
    const result = await response.json();
    document.getElementById("feedback").textContent = "Error: " + result.errors.join(" ");
    document.getElementById("feedback").style.color = "red";
  } else {
    window.location.reload();
  }
  document.getElementById('contractForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const contractName = document.getElementById('contractName').value;
    const contractDetails = document.getElementById('contractDetails').value;

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            contract_name: contractName,
            contract_details: contractDetails
        })
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server
        alert(data.result);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

});
});
