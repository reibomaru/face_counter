const display_count = document.getElementById('display_count')
const display_time = document.getElementById('display_time')
let runtime = 0

window.setInterval(refreshHTML, 1000);

function refreshHTML() {
    $.getJSON("/static/count.json", function (json) {
        console.log(json.face_count)
        display_count.textContent = json.face_count
    })
    display_time.textContent = runtime++
}

