const display_face_count = document.getElementById('display_face_count')
const display_eye_count = document.getElementById('display_eye_count')
const display_face_only_count = document.getElementById('display_face_only_count')
const display_start_date = document.getElementById('display_start_date')
const display_start_time = document.getElementById('display_start_time')

let face_count_data = {
    face_count: 0,
    eye_count: 0,
    start_unix_time: null,
}

const httpRequest = new XMLHttpRequest();

document.addEventListener('DOMContentLoaded', function () {
    renderHTMLFromData(face_count_data)
    let intervalID
    intervalID = setInterval(function () {
        intervalRendering().then(
            function (response) {
                renderHTMLFromData(response)
            },
            function () {
                renderHTMLFromData(face_count_data)
                alert('カウントを終了します。')
                clearInterval(intervalID)
            }
        )
    }, 3000);
})

function intervalRendering() {
    return new Promise(function (resolve,reject) {
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4) {
                if (httpRequest.status === 200) {
                    let json = JSON.parse(httpRequest.responseText || 'null')
                    resolve(json)
                } else {
                    alert('データが読み込めませんでした')
                    reject()
                }
            }
        }
        httpRequest.open('POST', "/static/face_count.json");
        httpRequest.send();
    })
}

function renderCount(data) {
    let face_only_count = null
    display_face_count.textContent = data.face_count
    display_eye_count.textContent = data.eye_count
    face_only_count = data.face_count - data.eye_count
    display_face_only_count.textContent = face_only_count
}

function renderHTMLFromData(data) {
    if (data === null) {
        data = face_count_data
    }
    renderCount(data)
    renderStartDateAndTime(data.start_unix_time)
}

function renderStartDateAndTime(unixtime) {
    if (unixtime === null) {
        display_start_date.textContent = '----/-/-'
        display_start_time.textContent = '--:--:--'
        return
    }
    let dateTime = new Date(unixtime * 1000);
    display_start_date.textContent = dateTime.toLocaleDateString('ja-JP')
    display_start_time.textContent = dateTime.toLocaleTimeString('ja-JP')
}
