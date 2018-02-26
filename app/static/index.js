var _ = function(el){
    return document.querySelector(el);
}


var _get = function (url, callback) {

    var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    xhr.open('GET', url);
    xhr.onreadystatechange = function () {
        if (xhr.readyState > 3 && xhr.status == 200) callback(xhr.responseText);
    };
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.send();
    return xhr;
}

var _post = function (url, data, callback) {
    var params = typeof data == 'string' ? data : Object.keys(data).map(
        function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }
    ).join('&');

    var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
    xhr.open('POST', url);
    xhr.onreadystatechange = function () {
        if (xhr.readyState > 3 && xhr.status == 200) { callback(xhr.responseText); }
    };
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(params);
    return xhr;
}



_('.s-theme').addEventListener('change',function(e){
    e.preventDefault();
    document.body.className = e.target.value;
});




_('.o-settings').addEventListener('click',function(e){
    e.preventDefault();
    _('.wrapper').className = 'wrapper tags-is-visible';
});
_('.o-addnew').addEventListener('click',function(e){
    e.preventDefault();
    _('.content').innerHTML = 'New Content';
});

_('.o-search').addEventListener('keydown',function(e){
    console.dir(e.target.value);
});

_('.o-login').addEventListener('click',function(e){
    e.preventDefault();
    _('.content').innerHTML = 'login';
});
_('.o-info').addEventListener('click',function(e){
    e.preventDefault();
    _('.wrapper').className = 'wrapper info-is-visible';
});
_('.o-list').addEventListener('click',function(e){
    e.preventDefault();
    _('.wrapper').className = 'wrapper';
});



_('.c-close').addEventListener('click',function(e){
    e.preventDefault();
    _('.wrapper').className = 'wrapper';
});
_('.c-tags').addEventListener('click',function(e){
    e.preventDefault();
    _('.wrapper').className = 'wrapper';
});

_('.overlay').addEventListener('click',function(e){
    e.preventDefault();
    _('.wrapper').className = 'wrapper';
});



/*
var settings = '',
    main = document.querySelector('main'),
    get_test = document.querySelector('.get_test'),
    post_test = document.querySelector('.post_test');


get_test.addEventListener('click', function (e) {
    e.preventDefault();
    var settings = ''
    _get(_CONFIG_, function (r) {
        settings = JSON.parse(r);
        main.innerHTML = settings.name;
    });
});



post_test.addEventListener('click', function (e) {
    e.preventDefault();
    var data = {
        title: 'Hello World'
    };
    _post('./test', JSON.stringify(data), function (r) {
        main.innerHTML = r;
    });
});
*/
