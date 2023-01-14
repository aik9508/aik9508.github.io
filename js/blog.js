jQuery(function() {
    $('.blog-more').on('click', function(){
        $('.blog-content').addClass('blog-hidden');
        var title = $(this).parent();
        var item = $(this).parent().parent();
        var lessbtn = title.children().eq(2);
        $(this).addClass('blog-hidden');
        var content = item.children().eq(1);
        content.removeClass('blog-hidden');
        lessbtn.removeClass('blog-hidden');
    });

    $('.blog-less').on('click', function(){
        var title = $(this).parent();
        var item = $(this).parent().parent();
        var morebtn = title.children().eq(1);
        $(this).addClass('blog-hidden');
        var content = item.children().eq(1);
        content.addClass('blog-hidden');
        morebtn.removeClass('blog-hidden');
    });
});