document.addEventListener('DOMContentLoaded', () => {
    const btnntt = document.getElementById('ttt'); // Nút Thêm nhân viên
    const btndong = document.getElementById('dong'); // Nút đóng (X) của form
    const form = document.getElementById('formtt'); // Form cần hiển thị hoặc ẩn
    let form_open = false; // Biến kiểm tra trạng thái form

    btnntt.addEventListener('click', () =>{
        if(!form_open){
            form.style.display = 'block';
            form_open = true;
        }else{
            form.style.display = 'none';
            form_open = false;
        }
    });
    


    btndong.addEventListener('click', () => {
        form.style.display = 'none';
        form_open = false;
    })
});
