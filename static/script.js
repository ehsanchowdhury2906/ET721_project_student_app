document.addEventListener('DOMContentLoaded', function() {

    // auto-hide flash messages after 3 seconds
    var flashMessages = document.querySelectorAll('.flash_msg');
    flashMessages.forEach(function(msg) {
        setTimeout(function() {
            msg.style.display = 'none';
        }, 3000);
    });

    // confirm before delete (only links, not buttons)
    var deleteLinks = document.querySelectorAll('a.btn_delete');
    deleteLinks.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this?')) {
                e.preventDefault();
            }
        });
    });

    // image preview modal
    var modal = document.getElementById('imgModal');
    var modalImg = document.getElementById('modalImg');
    var modalSubject = document.getElementById('modalSubject');
    var modalDownload = document.getElementById('modalDownload');
    var closeBtn = document.getElementById('closeModal');

    if (modal) {
        var imgs = document.querySelectorAll('.preview_img');
        imgs.forEach(function(img) {
            img.addEventListener('click', function() {
                modal.style.display = 'flex';
                modalImg.src = this.src;
                modalSubject.innerText = this.dataset.subject;
                modalDownload.href = this.src;
            });
        });

        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }

});