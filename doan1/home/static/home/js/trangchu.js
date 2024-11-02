document.addEventListener('DOMContentLoaded', function(){
    // Sidebar toggle
    // const btnsider = document.getElementById('btn-sidebar');
    // const sidebar = document.getElementById('sidebar');
    // let sbopen = false;
    // btnsider.addEventListener('click', () => {
    //     if(sbopen){
    //         sidebar.style.left = '-300px';
    //         sbopen = false;
    //     }else{
    //         sidebar.style.left = '0';
    //         sbopen = true;
    //     }
    // });

  
    const subMenus = document.querySelectorAll('.item > li > a');
    subMenus.forEach(menu => {
        menu.addEventListener('click', (e) => {
            e.preventDefault();
            const subMenu = menu.nextElementSibling;
            if (subMenu.style.display === 'block') {
                subMenu.style.display = 'none';
            } else {
                subMenu.style.display = 'block';
            }
        });
    });

});

function navigateTo(path) {
    window.location.href = `http://127.0.0.1:8000${path}`;
}
