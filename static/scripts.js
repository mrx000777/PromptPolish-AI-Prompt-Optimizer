document.getElementById("optimizeBtn").addEventListener("click", async () => {
  const prompt = document.getElementById("userPrompt").value.trim();
  const resultDiv = document.getElementById("result");
  const optimizedText = document.getElementById("optimizedPrompt");
  const loadingDiv = document.getElementById("loading");

  if (!prompt) {
    alert("Please enter a prompt first!");
    return;
  }

  resultDiv.classList.add("hidden");
  loadingDiv.classList.remove("hidden");

  try {
    const response = await fetch("/optimize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    const data = await response.json();

    loadingDiv.classList.add("hidden");
    optimizedText.textContent = data.optimized_prompt || "No response from AI.";
    resultDiv.classList.remove("hidden");
  } catch (error) {
    loadingDiv.classList.add("hidden");
    optimizedText.textContent = "⚠️ Error optimizing prompt. Please try again.";
    resultDiv.classList.remove("hidden");
  }
});
