const input = document.getElementById("message");
const hello = document.getElementById("hello");

input.addEventListener("input", () => {
    if (input.value.trim() !== "") {
        hello.style.opacity = "0";
    } else {
        hello.style.opacity = "1";
    }
});

const handleSend = async () => {
    let question = input.value.trim();
    if (question === "") return;

    try {
        const response = await fetch(`/get_dimension?query=${encodeURIComponent(question)}`);
        const data = await response.json();
        if (data.success) {
            alert(`Dimension: ${data.formula}`);
        } else {
            alert("Not found in database.");
        }
    } catch (e) {
        console.error("Error:", e);
    }
    input.value = "";
    hello.style.opacity = "1";
};

