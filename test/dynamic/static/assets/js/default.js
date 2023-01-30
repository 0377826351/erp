$(document).ready(function(){
    setHeightTableContent();
});
// Height table content
function setHeightTableContent(){
    const offsetHeight = $('#header').outerHeight() + $('.page-title').outerHeight() + $('.filter-box').outerHeight() + $('.table-pagination').outerHeight();
    $('.table-content').css('max-height', 'calc(100vh - ' + (offsetHeight + 1) + 'px - 5rem)')
}
// Check element has attr?
function checkHasAttr(element, key) {
    var attr = element.attr(key);
    return typeof attr !== 'undefined' && attr !== false;
}
// change per_page select
function changePerPage(number) {
    window.location.replace(updateQueryStringParameter(window.location.href, 'per_page', number));
}
// Update url with query string
function updateQueryStringParameter(uri, key, value) {
    var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
    var separator = uri.indexOf('?') !== -1 ? "&" : "?";
    if (uri.match(re)) {
      return uri.replace(re, '$1' + key + "=" + value + '$2');
    }
    else {
      return uri + separator + key + "=" + value;
    }
}
