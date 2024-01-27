const cells = document.getElementsByTagName("td");
for (const cell of cells) {
    var text = cell.innerText;
    if (text.toLowerCase().includes("free")) {
        if (cells.length === 25) {
            cell.style.fontSize = "14pt";
        } else if (cells.length === 16) {
            cell.style.fontSize = "20pt";
        } else {
            cell.style.fontSize = "25pt";
        }
        cell.style.fontWeight = "bold";
    }
}