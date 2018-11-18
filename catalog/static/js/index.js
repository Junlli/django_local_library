// 鼠标点击导航栏触发事件
$(function () {
    $(".nav li").on('click', function () {
        // console.log($(".book-introduct").length);
        $(this).addClass('nav-bgcolor').siblings().removeClass('nav-bgcolor');
    })

    if ($(".book-introduct").length >= 2) {
        $('.pagination').show();
    }
})


