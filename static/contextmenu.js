// var $j = jQuery.noConflict();

// Функция для определения координат указателя мыши
function defPosition(event) {
    var x = y = 0;
    var d = document;
    var w = window;

    if (d.attachEvent != null) { // Internet Explorer & Opera
        x = w.event.clientX + (d.documentElement.scrollLeft ? d.documentElement.scrollLeft : d.body.scrollLeft);
        y = w.event.clientY + (d.documentElement.scrollTop ? d.documentElement.scrollTop : d.body.scrollTop);
    } else if (!d.attachEvent && d.addEventListener) { // Gecko
        x = event.clientX + w.scrollX;
        y = event.clientY + w.scrollY;
    }

    return {x:x, y:y};
}

function menu(event) {
    // Блокируем всплывание события contextmenu
    event = event || window.event;
    event.cancelBubble = true;

    var elem = event.target.closest('.draggable');

    var rm = $(".right-menu");

    rm.empty();
    rm.append('<div class="w-100 btn btn-lg btn-danger" onclick="setToBasket(\'' + elem.id + '\')">Поместить в корзину</div>');
    rm.append('<div class="w-100 btn btn-lg btn-primary" onclick="rename(\'' + elem.id + '\', \'' + elem.innerHTML + '\')">Переименовать</div>');
    rm.append('<div class="w-100 btn btn-lg btn-primary" onclick="editText(\'' + elem.id + '\', \'' + elem.innerHTML + '\')">Редактировать</div>');
    if(!elem.classList.contains('droppable')){
        rm.append('<div class="w-100 btn btn-lg btn-primary" onclick="createExternalLink(\'' + elem.id + '\', \'' + elem.innerHTML + '\')">Создать внешнюю ссылку</div>');
    }

    // Задаём позицию контекстному меню
    var menu = $('.right-menu').css({
        top: defPosition(event).y + "px",
        left: defPosition(event).x + "px"
    });

    // Показываем собственное контекстное меню
    menu.show();

    // Блокируем всплывание стандартного браузерного меню
    return false;
}

// Закрываем контекстное при клике правой кнопкой по документу
$(document).on('contextmenu', function(){
    $('.right-menu').hide();
});

// Закрываем контекстное при клике левой кнопкой по документу
$(document).on('click', function(){
    $('.right-menu').hide();
});
