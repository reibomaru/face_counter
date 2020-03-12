const display_count = document.getElementById('display_count')
const display_time = document.getElementById('display_time')
let runtime = 0
let face_count = 0

window.setInterval(refreshHTML, 1000);

function refreshHTML() {
    $.post("/static/face_count.json", function (json) {
        console.log(json.face_count)
        face_count = json.face_count
        display_count.textContent = face_count
    })
    display_time.textContent = runtime++
}

