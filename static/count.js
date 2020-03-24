const display_face_count = document.getElementById('display_face_count')
const display_eye_count = document.getElementById('display_eye_count')
const display_face_only_count = document.getElementById('display_face_only_count')
const display_start_date = document.getElementById('display_start_date')
const display_start_time = document.getElementById('display_start_time')
const count_start_btn = document.getElementById('count_start_btn')
const count_stop_btn = document.getElementById('count_stop_btn')

let face_count_data = {
    face_count: 0,
    eye_count: 0,
    start_unix_time: null,
}

let intervalID = null

const httpRequest = new XMLHttpRequest();

document.addEventListener('DOMContentLoaded', function () {
    renderHTMLFromData(face_count_data)
})

count_start_btn.addEventListener('click', function () { 
    sendStart().then(
        function () {
            console.log('正常にカウントは開始されました。')
        },
        function () {
            console.log('カウントの開始に異常がありました。')
            clearInterval(intervalID)
        }
    ).then(
        function () {
            intervalID = setInterval(function () {
                getJSON().then(
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
        }
    )
})

count_stop_btn.addEventListener('click', function () {
    sendStop().then(
        function () {
            console.log('正常にカウントは停止されました。')
            clearInterval(intervalID)
        },
        function () {
            console.log('カウントの停止に異常がありました。')
            clearInterval(intervalID)
        }
    )
})

function sendStart() {
    return new Promise(function (resolve, reject) {
        httpRequest.open('GET', '/face_count/start_count/')
        httpRequest.send()
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4) {
                console.log(httpRequest.status)
                if (httpRequest.status === 200) {
                    resolve()
                } else {
                    console.log('エラー')
                    reject()
                }
            }
        }
    })
}

function sendStop() {
    return new Promise(function (resolve, reject) {
        httpRequest.open('GET', '/face_count/stop_count/')
        httpRequest.send()
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4) {
                if (httpRequest.status === 200) {
                    resolve()
                } else {
                    reject()
                }
            }
        }
    })
}

function getJSON() {
    return new Promise(function (resolve, reject) {
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4) {
                if (httpRequest.status === 200) {
                    let json = JSON.parse(httpRequest.responseText || 'null')
                    resolve(json)
                } else {
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
