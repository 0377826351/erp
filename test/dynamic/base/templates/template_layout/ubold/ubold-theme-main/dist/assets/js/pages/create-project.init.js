!function(o){"use strict";var t=function(){this.$body=o("body")};t.prototype.init=function(){Dropzone.autoDiscover=!1,o('[data-plugin="dropzone"]').each(function(){var t=o(this).attr("action"),e=o(this).data("previewsContainer"),a={url:t};e&&(a.previewsContainer=e);var i=o(this).data("uploadPreviewTemplate");i&&(a.previewTemplate=o(i).html());o(this).dropzone(a)})},o.FileUpload=new t,o.FileUpload.Constructor=t}(window.jQuery),function(t){"use strict";window.jQuery.FileUpload.init()}(),$('[data-toggle="select2"]').select2(),$('[data-toggle="flatpicker"]').flatpickr({altInput:!0,altFormat:"F j, Y",dateFormat:"Y-m-d"});