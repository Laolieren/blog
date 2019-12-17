var cur_page = 1; // 当前页
var next_page = 1; // 下一页
var total_page = 1;  // 总页数
var live_data_querying = true;   // 是否正在向后台获取数据

function updateLivesData(action,limit=10) {
    var params = {
        page: next_page,
        limit: limit
    };
    $.get("/api/v1_0/lives", params, function (resp) {
        live_data_querying = false;
        if (resp.errno == 0) {
            if (0 == resp.data.total_page) {
                $(".live-list").html("暂时没有动态");
            } else {
                total_page = resp.data.total_page;
                if ("renew" == action) {
                    cur_page = 1;
                    $(".live-list").html(template("live-list-tmpl", {lives: resp.data.lives}));
                } else {
                    cur_page = next_page;
                    $(".live-list").append(template("live-list-tmpl", {lives: resp.data.lives}));
                }
            }
        }
    })
}
$(document).ready(function () {
    var mySwiper = new Swiper('.swiper-container', {
        loop: true, // 循环模式选项
        speed: 300,
        autoplay: {
            disableOnInteraction: false,
            delay: 1000
        },
        effect: 'fade',
        fadeEffect: {
            crossFade: true,
        },
        // 如果需要分页器
        pagination: {
            el: '.swiper-pagination',
        },

        // 如果需要前进后退按钮
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },

    });
    // 首页轮播图鼠标进入停止离开继续轮播
    $('.swiper-container').mouseenter(function () {
        mySwiper.autoplay.stop();
    }).mouseleave(function () {
        mySwiper.autoplay.start();
    })

    $(".newslist").on("mouseenter", "li", function () {
        $(".newslist li").removeClass("showActive")
        $(this).addClass("showActive")
    }).on("mouseleave", "li", function () {
        $(this).removeClass("showActive");
        var isShow = 0;
        if ($(".newslist li").hasClass("showActive")) {
            isShow += 1
        }
        if (isShow == 0) {
            $(".newslist li:first-of-type").addClass("showActive")
        }
    })
})