var display = null;

function PDFDisplay() {
    this.pdfObj = {
        'canvasId': null,
        'isPageRendering': false,
        'numPages': null,
        'pageNum': 1,
        'pageNumPending': null,
        'pdf': null,
        'scale': 1.5
    };
};

PDFDisplay.prototype.display_pdf = function(pdf_url, canvasId) {
    display = this;
    this.pdfObj.canvasId = canvasId;

    try {
        PDFJS.getDocument(pdf_url).then(function getPdf(pdfDoc) {
            display.pdfObj.pdf = pdfDoc;
            display.pdfObj.numPages = display.pdfObj.pdf.numPages;

            if (display.pdfObj.numPages > 1) {
                var pdf_id = display.pdfObj.canvasId;

                var list = $('ul#' + pdf_id + '-pagination');

                var li = $('<li/>').addClass('arrow').appendTo(list);
                var link = $('<a/>').attr('id', 'previous').text('«').appendTo(li);
                link.on('click', function() {
                    if (display.pdfObj.pageNum <= 1) {
                        return;
                    }

                    $('#' + pdf_id + '-page-' + display.pdfObj.pageNum).parent().removeClass('current');
                    display.pdfObj.pageNum--;
                    display.queueRenderPage(display.pdfObj.pageNum);
                    $('#' + pdf_id + '-page-' + display.pdfObj.pageNum).parent().addClass('current');
                });

                for (var n = 1; n <= display. pdfObj.numPages; n++) {
                    var cssClass = 'page';

                    if (n == 1) {
                        cssClass += ' current';
                    }

                    li = $('<li/>').addClass(cssClass).appendTo(list);
                    link = $('<a/>').attr('id', pdf_id + '-page-' + n).text(n).appendTo(li);
                    link.on('click', function() {
                        $('li.current').removeClass('current');
                        display.pdfObj.pageNum = parseInt($(this).text(), 10);
                        display.queueRenderPage(display.pdfObj.pageNum);
                        $('#' + display.pdfObj.canvasId + '-page-' + display.pdfObj.pageNum).parent().addClass('current');
                    });
                }

                li = $('<li/>').addClass('arrow').appendTo(list);
                link = $('<a/>').attr('id', pdf_id + '-next').text('»').appendTo(li);
                link.on('click', function() {
                    if (display.pdfObj.pageNum >= display.pdfObj.numPages) {
                        return;
                    }

                    $('#' + pdf_id + '-page-' + display.pdfObj.pageNum).parent().removeClass('current');
                    display.pdfObj.pageNum++;
                    display.queueRenderPage(display.pdfObj.pageNum);
                    $('#' + pdf_id + '-page-' + display.pdfObj.pageNum).parent().addClass('current');
                });
            } else {
                $('#' + display.pdfObj.canvasId + '-pagination').parent().parent().remove();
            }

            // Initial/first page rendering
            display.renderPage(display.pdfObj.pdf, display.pdfObj.pageNum, display.pdfObj.canvasId);
        });
    } catch(e) {
        display_pdf_error_handler();
    }
};

/**
 * If another page rendering in progress, waits until the rendering is
 * finised. Otherwise, executes rendering immediately.
 */
PDFDisplay.prototype.queueRenderPage = function(pageNum) {
    if (this.pdfObj.isPageRendering) {
        this.pdfObj.pageNumPending = pageNum;
    } else {
        this.renderPage(this.pdfObj.pdf, pageNum, this.pdfObj.canvasId);
    }
};

/**
 * Get page info from document, resize canvas accordingly, and render page.
 * @param pageNum Page number.
 */
PDFDisplay.prototype.renderPage = function(pdf, pageNum, canvasId) {
    var display = this;
    this.pdfObj.isPageRendering = true;

    // Using promise to fetch the page
    pdf.getPage(pageNum).then(function(page) {
        var viewport = page.getViewport(display.pdfObj.scale);

        var canvas = document.getElementById(canvasId);
        var context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        // Render PDF page into canvas context
        var renderContext = {
            canvasContext: context,
            viewport: viewport
        };

        var renderTask = page.render(renderContext);

        // Wait for rendering to finish
        renderTask.promise.then(function() {
            display.pdfObj.isPageRendering = false;

            if (display.pdfObj.pageNumPending !== null) {
                // New page rendering is pending
                this.renderPage(display.pdfObj.pageNumPending);
                display.pdfObj.pageNumPending = null;
            }
        });
    });
};

function display_pdf_error_handler() {
    $('#pdf-canvas-pagination').parent().parent().remove();
    $('#pdf-canvas').attr('height', '60px');
    $('#pdf-canvas').attr('width', '300px');
}
