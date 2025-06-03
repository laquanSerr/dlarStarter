
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contract-form");
  const feedback = document.getElementById("feedback");
  const container = document.getElementById("contracts");

  // 🔄 Load contracts on page load
  async function loadContracts() {
    try {
      const res = await fetch("/contracts");
      const contracts = await res.json();
      container.innerHTML = ""; // Clear previous content

      if (contracts.length === 0) {
        container.textContent = "No contracts submitted yet.";
        return;
      }

      contracts.forEach((contract, index) => {
        const div = document.createElement("div");
        div.classList.add("contract-entry");

        const html = `
          <p><strong>DAD:</strong> ${contract.dad}</p>
          <p><strong>Status:</strong> ${contract.status}</p>
        `;
        div.innerHTML = html; // Set before button to avoid overwrite

        // ✅ Only show button if status is "submitted"
        if (contract.status === "submitted") {
          const button = document.createElement("button");
          button.textContent = "Mark as Completed";
          button.classList.add("complete-btn");
          button.dataset.index = index;

          button.addEventListener("click", async () => {
            try {
              const res = await fetch("/complete", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json"
                },
                body: JSON.stringify({ index })
              });

              const result = await res.json();
              if (res.ok) {
                alert(result.message);
                window.location.reload();
              } else {
                alert("Error: " + result.message);
              }
            } catch (err) {
              console.error("Error completing contract:", err);
              alert("Unexpected error.");
            }
          });

          div.appendChild(button);
        }

        container.appendChild(div);
      });
    } catch (err) {
      console.error("Failed to load contracts:", err);
      container.textContent = "Failed to load contracts.";
    }
  }

  // 📤 Submit new contract
 form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const dadText = document.getElementById("dad-input").value.trim();

  // Live validation
  if (!dadText) {
    feedback.textContent = "❌ Please enter a DAD.";
    return;
  }
  if (dadText.length > 5000) {
    feedback.textContent = "❌ DAD exceeds max length (5000 characters).";
    return;
  }

  try {
    const res = await fetch("/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dad: dadText })
    });

    const result = await res.json();
    if (res.ok) {
      feedback.textContent = "✅ Contract submitted.";
      form.reset();
      loadContracts();
    } else {
      feedback.textContent = `❌ ${result.message || "Submission failed."}`;
    }
  } catch (err) {
    console.error("Submit error:", err);
    feedback.textContent = "❌ Network or server error.";
  }
});


  loadContracts(); // Initial load
});


