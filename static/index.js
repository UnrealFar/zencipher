
function show(el_id) {
    var e = document.getElementById(el_id);
    if e.style.visibilty == "hidden" {
        e.style.visibilty = "visible";
    } else {
        e.style.visibilty = "hidden";
    }
}
