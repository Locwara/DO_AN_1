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
    const btnimport = document.getElementById('import');
    const btndongimport = document.getElementById('dongimport');
    const form_import = document.getElementById('form_import_thongtinnhanvien');
    let form_import_open = false;

    btnimport.addEventListener('click', () =>{
        if(!form_import_open){
            form_import.style.display = 'block';
            form_import_open = true;
        }else{
            form_import.style.display = 'none';
            form_import_open = false;
        }
    });

    btndongimport.addEventListener('click', () =>{
        form_import.style.display = 'none';
        form_import_open = false;
    });
});
