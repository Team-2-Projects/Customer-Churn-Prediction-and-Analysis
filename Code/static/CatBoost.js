document.getElementById('churnForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const customerID = document.getElementById('customerID').value;

    const response = await fetch(`/predict?customerID=${customerID}`);
    const data = await response.json();

    document.getElementById('result').innerHTML = `
        Customer ID: ${customerID} <br>
        Churn Risk: ${data.prediction} <br>
        Probability: ${(data.probability * 100).toFixed(2)}%
    `;
});
