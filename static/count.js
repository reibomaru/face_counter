const display_face_count = document.getElementById('display_face_count')
const display_eye_count = document.getElementById('display_eye_count')
const display_face_only_count = document.getElementById('display_face_only_count')
const display_start_date = document.getElementById('display_start_date')
const display_start_time = document.getElementById('display_start_time')

let runtime = 0
let face_count = 0
let eye_count = 0
let face_only_count = 0
let dateText = ''
let timeText = ''

document.addEventListener('DOMContentLoaded', function () {
    setInterval(function () {
        intervalRendering().then(
            function (response) {
                postHandler(response)
            },
            function (error) {
                console.log(error)
            }
        )
    }, 3000);
})

function intervalRendering() {
    return new Promise(function (resolve) {
        $.post("/static/face_count.json", function (json) {
            return resolve(json)
        })
    })
}

function postHandler(json) {
    [dateText, timeText] = renderStartDateAndTime(json.start_unix_time)
    display_start_date.textContent = dateText
    display_start_time.textContent = timeText
    face_count = json.face_count
    eye_count = json.eye_count
    face_only_count = face_count - eye_count
    display_face_count.textContent = face_count
    display_eye_count.textContent = eye_count
    display_face_only_count.textContent = face_only_count
}

function renderStartDateAndTime(unixtime) {
    let dateTime = new Date(unixtime * 1000);
    return [dateTime.toLocaleDateString(), dateTime.toLocaleTimeString('ja-JP')]
}
