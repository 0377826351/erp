$(document).ready(function(){
    $("input").keyup(function(e) {
        var name = $("#name").val();
        var phone = $("#phone").val();
        var address = $("#address").val()
        var mail = $("#mail").val();
        var content = $("#content").val();
        if (name != '' || phone != '' || address != ''){
            $("button").attr("disabled", false);
        }
    });
    $(".btn-send").click(function(e){
      e.preventDefault(); //xoa chuc nang dang thuc hien
      var isError = false; 
      var str = "<ul>";
      if ($("#name").val() == '') {
        isError = true;
        str += "<li>- Bạn cần nhập tên</li>";
      };
      if ($("#phone").val() == '') {
        isError =true;
        str += "<li>- Bạn cần số điện thoại</li>";
      };
      if ($("#address").val() == '') {
        isError = true;
        str += "<li>- Bạn cần nhập địa chỉ</li>";
      };
      str += '</ul>';
      $(".notification").html(str);
      console.log(isError);
      if (!isError){
        $('form').submit();
      }
    });
});