function show_add() {
    document.getElementById("add-service-model").style.display = 'block'
}

function show_edit() {
    document.getElementById("edit-service-model").style.display = 'block'
}

document.querySelectorAll("#service").forEach((item) => {
    item.addEventListener('click', function(e) {
        document.getElementById("servicein").value = e.target.innerHTML;
        document.getElementById("oldservice").value = e.target.value;
        document.getElementById("amountin").value = e.target.dataset.value1;
        document.getElementById("linkin").value = e.target.dataset.value4;
        document.getElementById("datein").value = (e.target.dataset.value3+"").replaceAll("/", "-");
    })

    
})

window.onclick = function(e) {
    if (e.target == document.getElementById("add-service-model")) {
        document.getElementById("add-service-model").style.display = 'none'
    }

    else if (e.target == document.getElementById("edit-service-model")) {
        document.getElementById("edit-service-model").style.display = 'none'
    }
 }

