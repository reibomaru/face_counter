const display_face_count = document.getElementById('display_face_count')
const display_eye_count = document.getElementById('display_eye_count')
const display_face_only_count = document.getElementById('display_face_only_count')
const display_start_date = document.getElementById('display_start_date')
const display_start_time = document.getElementById('display_start_time')
const count_start_btn = document.getElementById('count_start_btn')
const count_stop_btn = document.getElementById('count_stop_btn')
const count_terminate_btn = document.getElementById('count_terminate_btn')
const count_restart_btn = document.getElementById('count_restart_btn')
const active_camera_btn = document.getElementById('active_camera_btn')
const deactive_camera_btn = document.getElementById('deactive_camera_btn')

const player = document.getElementById('player');
const snapshot_canvas = document.getElementById('snapshot_canvas');
const result_canvas = document.getElementById('result_canvas')
let videoTracks = null

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
    setStatusToInactive()
    navigator.mediaDevices.getUserMedia(
        { video: { width: 1280, height: 720 } }
    ).then(handleSuccess);
})

active_camera_btn.addEventListener('click', function () {
    navigator.mediaDevices.getUserMedia(
        { video: { width: 1280, height: 720} }
    ).then(handleSuccess);                                                                                                                                    
    setStatusToInactive()
})

deactive_camera_btn.addEventListener('click', function () {
    for (let i = 0; i < videoTracks.length; i++){
        videoTracks[i].stop()
    }
    setStatusToInactiveAll()
})

count_start_btn.addEventListener('click', function () {
    renderHTMLFromData(face_count_data)
    sendStart().then(
        function () {},
        function () {
            clearInterval(intervalID)
        }
    ).then(
        function () {
            setStatusToCounting()
            intervalID = setInterval(function () {
                captureSnapshotAndSendImg().then(
                    function (response) {
                        renderImageFromBase64(response.img_base64)
                        renderHTMLFromData(response)
                    },
                    function () {
                        renderHTMLFromData(face_count_data)
                        alert('カウントを終了します。')
                        setStatusToInactive()
                        clearInterval(intervalID)
                    }
                )
            }, 3000);
        }
    )
})

count_stop_btn.addEventListener('click', function () {
    clearInterval(intervalID)
    setStatusToStopped()
})

count_restart_btn.addEventListener('click', function () {
    intervalID = setInterval(function () {
        captureSnapshotAndSendImg().then(
            function (response) {
                renderHTMLFromData(response)
            },
            function () {
                alert('カウントを終了します。')
                setStatusToInactive()
                clearInterval(intervalID)
            }
        )
    }, 3000);
    setStatusToCounting()
})

count_terminate_btn.addEventListener('click', function () {
    sendTerminate().then(
        function () {
            setStatusToInactive()
            clearInterval(intervalID)
        },
        function () {
            alert('カウントの停止に異常がありました。')
            setStatusToCounting()
            clearInterval(intervalID)
        }
    )
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
                    reject()
                }
            }
        }
    })
}

function sendTerminate() {
    return new Promise(function (resolve, reject) {
        httpRequest.open('GET', '/terminate_count/')
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

function handleSuccess(stream) {
    let mediaWidth = stream.getVideoTracks()[0].getSettings().width
    let mediaHeight = stream.getVideoTracks()[0].getSettings().height
    console.log(mediaWidth, mediaHeight)
    player.srcObject = stream
    videoTracks = stream.getVideoTracks();
    
    snapshot_canvas.width = mediaWidth
    snapshot_canvas.height = mediaHeight
    result_canvas.width = mediaWidth
    result_canvas.height = mediaHeight
    let ctx = snapshot_canvas.getContext('2d')
    ctx.fillStyle = 'silver';
    ctx.fillRect(0, 0, mediaWidth, mediaHeight);
    ctx = result_canvas.getContext('2d')
    ctx.fillStyle = 'silver';
    ctx.fillRect(0, 0, mediaWidth, mediaHeight);
};

function captureSnapshotAndSendImg() {
    const context = snapshot_canvas.getContext('2d')
    context.drawImage(player, 0, 0, snapshot_canvas.width, snapshot_canvas.height)
    return new Promise(function (resolve, reject) {
        const imgBlob = snapshot_canvas.toDataURL("image/png", 1.0);
        sendImg(imgBlob).then(
            function (response) {
                resolve(response)
            },
            function () {
                alert('画像が正常に送れないためカウントを終了します。')
                clearInterval(intervalID)
                reject()
            }
        )
    })

}

function sendImg(imgBlob) {
    return new Promise(function (resolve, reject) {
        formdata = new FormData()
        formdata.append('img', imgBlob)
        httpRequest.open('POST', '/send_img/')
        httpRequest.setRequestHeader("X-CSRFToken", csrftoken)
        httpRequest.send(formdata)
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

function renderImageFromBase64(base64) {
    const context = result_canvas.getContext('2d')
    const image = new Image();
    image.onload = function () {
        context.drawImage(image, 0, 0, result_canvas.width, result_canvas.height);
    };
    image.src = base64
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

function setStatusToInactive() {
    count_start_btn.disabled = false
    count_stop_btn.disabled = true
    count_restart_btn.disabled = true
    count_terminate_btn.disabled = true
    active_camera_btn.disabled = true
    deactive_camera_btn.disabled = false
}

function setStatusToInactiveAll() {
    count_start_btn.disabled = true
    count_stop_btn.disabled = true
    count_restart_btn.disabled = true
    count_terminate_btn.disabled = true
    active_camera_btn.disabled = false
    deactive_camera_btn.disabled = true
}

function setStatusToCounting() {
    count_start_btn.disabled = true
    count_stop_btn.disabled = false
    count_restart_btn.disabled = true
    count_terminate_btn.disabled = false
    active_camera_btn.disabled = true
    deactive_camera_btn.disabled = true
}

function setStatusToStopped() {
    count_start_btn.disabled = true
    count_stop_btn.disabled = true
    count_restart_btn.disabled = false
    count_terminate_btn.disabled = false
    active_camera_btn.disabled = true
    deactive_camera_btn.disabled = true
}
