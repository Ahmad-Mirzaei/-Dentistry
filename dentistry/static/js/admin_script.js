$(document).ready(function () {
    var listOfElements = $('select[id^="id_product_features-"][id$="-feature"]');
    $(listOfElements).on('change', function () {
        var f_id = $(this).val();
        var dd1 = $(this).attr('id');
        var dd2 = dd1.replace("-feature", "-filter_value");

        // Validate and encode f_id before using it in the URL
        if (!/^\d+$/.test(f_id)) {
            console.error("Invalid feature ID");
            return; // Exit if f_id is not a valid number
        }

        $.ajax({
            type: 'GET',
            url: "/products/ajax_admin/?feature_id=" + encodeURIComponent(f_id),
            success: function (res) {
                var cols = document.getElementById(dd2);
                cols.options.length = 0;

                // Sanitize and validate response data before inserting it into the DOM
                for (var k in res) {
                    if (res.hasOwnProperty(k)) {
                        var optionText = $('<div>').text(k).html(); // Sanitize the option text
                        var optionValue = $('<div>').text(res[k]).html(); // Sanitize the option value
                        cols.options.add(new Option(optionText, optionValue));
                    }
                }
            }
        });
    });
});

$(document).ready(function () {
    $('#id_product_name').on('input', function () {
        const productName = $(this).val();
        const slug = createSlug(productName);
        $('#id_slug').val(slug);
    });

    function createSlug(text) {
        return text
            .toLowerCase()                      // Convert to lowercase
            .trim()                             // Remove extra spaces from start and end
            .replace(/[\s]+/g, '-')            // Replace spaces with '-'
            .replace(/[^\w\-آ-ی۰-۹]+/g, '')    // Remove invalid characters (allow Persian letters and numbers)
            .replace(/\-\-+/g, '-')            // Replace '- -' with '-'
            .replace(/^-+|-+$/g, '');          // Remove '-' from start and end
    }
});