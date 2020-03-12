const display_face_count = document.getElementById('display_face_count')
const display_eye_count = document.getElementById('display_eye_count')
const display_time = document.getElementById('display_time')
let runtime = 0
let face_count = 0
let eye_count = 0

window.setInterval(refreshHTML, 1000);

function refreshHTML() {
    $.post("/static/face_count.json", function (json) {
        postHandler(json)
    })
    display_time.textContent = runtime++
}

function postHandler (json) {
    // console.log(json.face_count)
    face_count = json.face_count
    eye_count = json.eye_count
    display_face_count.textContent = face_count
    display_eye_count.textContent = eye_count
}