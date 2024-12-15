// function searchPatient() {
//     var value =  $("#q_disease").val();
//     $.get('/search/patient/' , {
//         value: value,
//     }).then(res => {
//         $("#disease_dev").text(res.diseaseName);
//         $("#id_diseases_0").val(res.diseaseId);
//     });
// }

$(document).ready(function() {
    $('.js-select-q_disease').select2();
});


function searchDisease() {  
    var value = $("#q_disease").val(); // خواندن ورودی کاربر  
    $.get('/search/disease/', { value: value })  
    .then(res => {  
        $("#disease_dev").empty(); // خالی کردن محتوای قبلی  
        $("#id_diseases_0").val(''); // خالی کردن ورودی شناسه  
        
        if (res.length === 0) {  
            $("#disease_dev").text("بیماری پیدا نشد"); // اگر هیچ بیماری پیدا نشد  
        } else {  
            res.forEach(disease => {  
                // ایجاد عنصر برای هر بیماری  
                $("#disease_dev").append(  
                    `<div class="disease-item" data-id="${disease.diseaseId}">  
                        ${disease.diseaseName}  
                    </div>`  
                );  
            });  

            // اضافه کردن رویداد کلیک برای انتخاب بیماری  
            $(".disease-item").click(function() {  
                var selectedId = $(this).data("id");  
                var selectedName = $(this).text();  
                $("#disease_dev").text(selectedName); // نمایش نام انتخاب شده  
                $("#id_diseases_0").val(selectedId); // قرار دادن شناسه انتخاب شده  
            });  
        }  
    })  
    .catch(error => {  
        console.error("Error fetching data:", error); // مدیریت خطاهای شبکه  
        $("#disease_dev").text("خطا در برقراری ارتباط"); // نمایش پیام خطا برای کاربر  
    });  
} 

function getSelectedDiseases() {  
    const selectElement = document.getElementById("q_disease"); // دسترسی به المان select  
    const selectedOptions = Array.from(selectElement.selectedOptions); // دریافت گزینه‌های انتخاب شده  
    const selectedValues = selectedOptions.map(option => option.value); // استخراج مقادیر  
    $.ajax({
        url: '/diseases/selected/',
        type: "GET",
        data: {  
            selected_values: JSON.stringify(selectedValues) // تبدیل آرایه به رشته جیسون  
        },  
        success: function(response) {  
            console.log("پاسخ موفق:", response);  
            // شما می‌توانید اینجا با پاسخ کار کنید  
        },  
        error: function(xhr, status, error) {  
            console.error("خطا در درخواست:", status, error);  
            // مدیریت خطا در اینجا  
        } 
    });
}

function deletePatient(patient_id) {
    const answer = confirm("آیا می‌خواهید بیمار را حذف کنید؟");
    if (answer) {
        $.ajax({
            url: "/accounts/delete_patient/",
            type: "GET",
            data: { patient_id: patient_id },
            success: function(res) {
                $("#table_patient").html(res);
            }
        });
    }
}

// function searchPatient() {
//     var value =  $("#q_patient").val();
//     $.ajax({
//         url: "/accounts/table_patients/",
//         type: "GET",
//         data: { value: value },
//         success: function(res) {
//             $("#search_result").html(res);
//         }
//     });
// }