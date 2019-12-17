/**
 * Created by python on 19-4-23.
 */

$(document).ready(function () {

    updateLivesData("renew");
    // 获取页面显示窗口的高度
    var windowHeight = $(window).height();
    // 为窗口的滚动添加事件函数
    window.onscroll = function () {
        // var a = document.documentElement.scrollTop==0? document.body.clientHeight : document.documentElement.clientHeight;
        var b = document.documentElement.scrollTop == 0 ? document.body.scrollTop : document.documentElement.scrollTop;
        var c = document.documentElement.scrollTop == 0 ? document.body.scrollHeight : document.documentElement.scrollHeight;
        // 如果滚动到接近窗口底部
        if (c - b < windowHeight + 50) {
            // 如果没有正在向后端发送查询房屋列表信息的请求
            if (!live_data_querying) {
                // 将正在向后端查询房屋列表信息的标志设置为真，
                live_data_querying = true;
                // 如果当前页面数还没到达总页数
                if (cur_page < total_page) {
                    // 将要查询的页数设置为当前页数加1
                    next_page = cur_page + 1;
                    // 向后端发送请求，查询下一页房屋数据
                    updateLivesData();
                } else {
                    live_data_querying = false;
                }
            }
        }
    };


    $("#etitle").focus(function () {
        $("#errmsg").hide();
    });
    $("#econtent").focus(function () {
        $("#errmsg").hide();
    });
    $(".myCommit").on("click", function () {
        var title = $("#etitle").val().trim();
        var content = $("#econtent").val().trim();
        if (!title) {
            $("#errmsg").html("请添加标题！").show();
            return;
        }
        if (!content) {
            $("#errmsg").html("请输入内容!").show();
            return;
        }
        var data = {
            title: title,
            content: content
        };
        var jsonData = JSON.stringify(data);
        $.ajax({
            url: "/api/v1_0/lives",
            type: "post",
            data: jsonData,
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.errno == 0) {
                    // 登录成功，跳转到主页
                    location.href = "/static/bloglist.html";
                    return;
                }
                else if (data.errno == 4105) {
                    location.href = "/static/login.html";
                    return;
                }
                else {
                    // 其他错误信息，在页面中展示
                    $("#errmsg").html(data.errmsg).show();
                    return;
                }
            }
        });
    })

});