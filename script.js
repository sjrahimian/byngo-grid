const cells = document.getElementsByTagName("td");
for (const cell of cells) {
    var text = cell.innerText;
    if (text.toLowerCase().includes("free")) {
        cell.style.fontSize = "15px";
    }
}