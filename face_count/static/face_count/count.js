const display_face_count = document.getElementById('display_face_count')
const display_eye_count = document.getElementById('display_eye_count')
const display_face_only_count = document.getElementById('display_face_only_count')
const display_start_date = document.getElementById('display_start_date')
const display_start_time = document.getElementById('display_start_time')
const count_start_btn = document.getElementById('count_start_btn')
const count_stop_btn = document.getElementById('count_stop_btn')

const player = document.getElementById('player');
const snapshotCanvas = document.getElementById('snapshot');
var videoTracks;


let face_count_data = {
    face_count: 0,
    eye_count: 0,
    start_unix_time: null,
}

let intervalID = null
const httpRequest = new XMLHttpRequest();
const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value

document.addEventListener('DOMContentLoaded', function () {
    renderHTMLFromData(face_count_data)
    navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 } })
        .then(handleSuccess);
})

const handleSuccess = function (stream) {
    console.log(stream)
    player.srcObject = stream;
    videoTracks = stream.getVideoTracks();
};

function captureSnapshotAndSendImg() {
    const context = snapshotCanvas.getContext('2d')
    context.drawImage(player, 0, 0, 640, 360)
    return new Promise(function (resolve, reject) {
        const imgBlob = snapshotCanvas.toDataURL("image/png", 1.0);
        console.log(imgBlob)
        sendImg(imgBlob).then(
            function (response) {
                console.log('画像が正常に送信できています')
                resolve(response)
            },
            function () {
                console.log('画像が正常に送れないためカウントを終了します。')
                clearInterval(intervalID)
                reject()
            }
        )
    })

}

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
                captureSnapshotAndSendImg().then(
                    function (response) {
                        console.log(response)
                        renderHTMLFromData(response)
                    },
                    function () {
                        renderHTMLFromData(face_count_data)
                        console.log('カウントを終了します。')
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
    videoTracks.forEach(function (track) { track.stop() });
})

function sendStart() {
    return new Promise(function (resolve, reject) {
        httpRequest.open('GET', '/start_count/')
        httpRequest.send()
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === 4) {
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
        httpRequest.open('GET', '/stop_count/')
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

function sendImg(imgBlob) {
    console.log('colled sendImg()')
    return new Promise(function (resolve, reject) {
        formdata = new FormData()
        formdata.append('img', imgBlob)
        formdata.append('height', snapshotCanvas.height)
        formdata.append('width', snapshotCanvas.width)
        httpRequest.open('POST', '/send_img/')
        httpRequest.setRequestHeader("X-CSRFToken", csrftoken)
        httpRequest.send(formdata)
        httpRequest.onreadystatechange = function () {
            console.log('response have come')
            if (httpRequest.readyState === 4) {
                if (httpRequest.status === 200) {
                    let json = JSON.parse(httpRequest.responseText || 'null')
                    resolve(json)
                } else {
                    reject()
                }
            }
        }
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