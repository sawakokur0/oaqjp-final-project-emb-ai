async function RunSentimentAnalysis() {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const output = document.getElementById("system_response");
    const query = new URLSearchParams({ textToAnalyze });

    try {
        const response = await fetch(`emotionDetector?${query}`);
        output.textContent = await response.text();
    } catch {
        output.textContent = "Unable to reach the application. Please try again.";
    }
}
