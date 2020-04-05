const comment_modal_btn = document.getElementById('comment_modal_btn')
const comment_modal = document.getElementById('comment_modal')

window.addEventListener('click', function (e) {
    if (e.target == comment_modal) {
        comment_modal.style.display = 'none';
    }
});

comment_modal_btn.addEventListener('click', function () {
    comment_modal.style.display = 'block'
})