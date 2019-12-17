/**
 * Created by python on 19-4-24.
 */

$(document).ready(function () {
    $.ajax({
        url: "/api/v1_0/session",
        type: "get",
        success: function (data) {
            if (data.errno == 0) {
                // 登录成功，跳转到主页
                $("#nologin").css("display", "none");
                $("#hadlogin").css("display", "block");
                return;
            }
            else {
                // 其他错误信息，在页面中展示
                $("#nologin").css("display", "block");
                $("#hadlogin").css("display", "none");
                return;
            }
        }
    });
    $("#hadlogin").on("click", "a", function () {
        $.ajax({
            url: "/api/v1_0/session",
            type: "delete",
            success: function (data) {
                location.href = "/";
                return
            }
        });
    });
    updateLivesData("renew", 6);
});
