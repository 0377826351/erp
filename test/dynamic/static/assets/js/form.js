$(document).ready(function() {
    init();
    setHeightTableContent();
    actionEvent();
    inputEvent();
    submitFilterForm();
    mapDeleteUrlToCofirmDialog();
    listViewDeleteItems();
    onChangeSelect2();
});

// Init
function init(){
    $('.select2').select2();
    $('body').on('click', '.select2-container', async function(){
        if ( $("span.select2-search .select2-search__field").length) $("span.select2-search .select2-search__field")[0].focus();
    });
    $('.select2-ajax').select2({
        language: "vi",
        minimumInputLength: 1,
        allowClear: true,
        placeholder: 'Nhập tên hoặc SĐT để tìm kiếm',
        ajax: {
            delay: 500,
            url: 'https://erp.nhatnamyvien.com/api2/shopf1/find-data',
            dataType: 'json',
            // data: function (params) {
            //     return { keyword: params.term }
            // },
            processResults: function (res, params) {
                data = res.data || []
                return {
                    results: $.map(data, function (item) {
                        return {
                            text: item.name + (item.phone ? ' - ' + item.phone : '') + (item.mobile ? ' - ' + item.mobile : ''),
                            id: item.id
                        };
                    })
                };
            }
        }
    });
    if ($( ".datepicker" ).length) {
        $('.datepicker').each(function(){
            const options = {
                dateFormat: 'dd/mm/yy'
            };
            if (checkHasAttr($(this), 'date-format')) options['dateFormat'] = $(this).attr('date-format')
            if (checkHasAttr($(this), 'max-date')) options['maxDate'] = $(this).attr('max-date')
            if (checkHasAttr($(this), 'min-date')) options['minDate'] = $(this).attr('min-date')
            $( ".datepicker" ).datepicker(options);
        });
    }
}
// Event Action
function actionEvent() {
    // check all
    $(".table-check-all").change(function() {
        $('.table-check-item').prop('checked', this.checked);
        checkActionMultiItems();
    });
    $(".table-check-item").change(function() {
        let checkAll = true;
        $(".table-check-item").each(function(){
            if (!this.checked){
                checkAll = false;
                return false;
            }
        });
        $('.table-check-all').prop('checked', checkAll);
        checkActionMultiItems();
    });
    // Check one item
    $('body').on('click', '.action-delete-item', function() {
        $(".table-check-all").prop('checked', false);
        const value = $(this).attr('value');
        $(".table-check-item").each(function(){
            $(this).prop('checked', $(this).attr('value') == value);
        });
    });
}

function checkActionMultiItems(){
    if ($('.table-check-item:checked').length) {
        $('.action-multi-items').show();
    } else {
        $('.action-multi-items').hide();
    }
}
// Event input
function inputEvent() {
    // Handle toggle password
    if($('.toggle-password').length) {
        $('body').on('click', '.toggle-password', function() {
            $(this).find('i').toggleClass('fa-eye-slash fa-eye');
            const inputType = $(this).parent().find('input').attr('type');
            $(this).parent().find('input').attr('type', (inputType == 'text' ? 'password' : 'text')).focus();
        });
    }
}

// Filter form
function submitFilterForm() {
    $('.form-filter .action-btn').click(function(e) {
        e.preventDefault();
        const form = $(this).parents('.form-filter');
        const type = $(this).attr('type');
        if (type == 'reset') { form.find('.form-control').val(''); }
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('per_page')) {
            form.append('<input type="hidden" name="per_page" value="'+ urlParams.get('per_page') +'" />');
        }
        $(this).parents('.form-filter').submit();
    });
}

// Map delete url to href confirm dialog
function mapDeleteUrlToCofirmDialog(){
    $('.table-content .delete-confirm').click(function(e) {
        e.preventDefault();
        const deleteUrl = $(this).attr('delete-url');
        const id = $(this).attr('data-bs-target');
        $(id + ' #diaglogConfirmButton').attr('href', deleteUrl);
        
    });
}

function listViewDeleteItems(){
    $('#confirmDeleteModel #diaglogConfirmButton').click(function(e) {
        e.preventDefault();
        const urlName = $('#listItems').attr('url-name');
        const deleteUrl = $('#listItems').attr('delete-url');
        let listItem = [];
        const csrf = $('input[name="csrfmiddlewaretoken"]').val();
        $('.table-check-item:checked').each(function() {
            listItem.push($(this).val());
        });
        let data = {
            'items_delete': listItem
        }
        $.ajax({
            type: "POST",
            url: deleteUrl,
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data),
            headers: { "X-CSRFToken": csrf },
            success: function(result){
                const status = result['status'];
                const message = result['message'];
                $('#diaglogCancelButton').hide();
                if (status == 'success'){
                    $('.btn-close').hide();
                    $('#confirmModelLabel').text('Xoá bản ghi thành công');
                    $('#confirmModelLabel').css('color', 'green');
                    $('.modal-body').text(message);
                    $('#diaglogConfirmButton').replaceWith($('<a class="btn btn-primary" href="' + window.location.href +'">Đóng</a>'));
                } else {
                    $('#confirmModelLabel').text('Xoá bản ghi thất bại');
                    $('#confirmModelLabel').css('color', 'red');
                    $('.modal-body').text(message);
                    $('#diaglogConfirmButton').text('Đóng');
                    $('#diaglogConfirmButton').attr('data-bs-dismiss', 'modal');
                }
            },
        });
    });
}

function onChangeSelect2(){
    $("[domain-invisible]").each(function (e) {
        const domainInvisible = JSON.parse($(this).attr('domain-invisible'));
        const elementInvisible = $('[data-name='+$(this).attr('name')+']');

        if (domainInvisible && domainInvisible.length) {
            domainInvisible.forEach(element => {
                if (Array.isArray(element) && element.length == 3 ) {
                    const name = element[0];
                    const operator = element[1];
                    const value = element[2];

                    if (checkInvisible(name, operator, value)) {
                        elementInvisible.hide();
                    } else {
                        elementInvisible.show();
                    }
                    
                    $("select[name='" + name + "']" ).on('change', function(){
                        if (checkInvisible(name, operator, value)) {
                            elementInvisible.hide();
                        } else {
                            elementInvisible.show();
                        }                
                    });
                }
            });
        }
    });
}

function checkInvisible (name, operator, value) {
    const selectValue =  $("select[name='" +name+ "']").val();
    if (value == "" || value.toLowerCase() == 'false' || value == false || value.toLowerCase() == 'none') {
        value = undefined
    }
    if (operator == '=') return (selectValue == value);
    if (operator == '!=') return (selectValue != value);
    if (operator == '>') return (selectValue > value);
    if (operator == '>=') return (selectValue >= value);
    if (operator == '<') return (selectValue < value);
    if (operator == '<=') return (selectValue <= value);
    if (operator == 'in') return (Array.isArray(value) && value.length && value.includes(selectValue));
    if (operator == 'not in') return (Array.isArray(value) && value.length && !value.includes(selectValue));
}