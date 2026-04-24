document.addEventListener('DOMContentLoaded', function() {
    // Navbar hündürlüyünü dinamik hesablamaq (opsional ehtiyat tədbiri)
    const nav = document.querySelector('.navbar');
    if (nav) {
        document.querySelector('.ms-profile-main-wrapper').style.paddingTop = (nav.offsetHeight + 30) + 'px';
    }
    
    // Bootstrap Modal işləkliyini yoxlamaq üçün (Redaktə et üçün)
    var myModal = document.getElementById('editProfileModal');
    if(myModal) {
        myModal.addEventListener('shown.bs.modal', function () {
            console.log('Modal açıldı!');
        });
    }
});