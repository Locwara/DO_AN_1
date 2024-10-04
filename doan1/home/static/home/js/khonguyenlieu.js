document.addEventListener('DOMContentLoaded', () =>{
    const btnntt = document.getElementById('tcl');
    const btndong = document.getElementById('dong');
    const form = document.getElementById('form_khonguyenlieu_ntt');
    let form_open = false;

    btnntt.addEventListener('click', () =>{
        if(!form_open){
            form.style.display = 'block';
            form_open = true;
        }else{
            form.style.display = 'none';
            form_open = false;
        }
    });

    btndong.addEventListener('click', () =>{
        form.style.display = 'none';
        form_open = false;
    });
});

