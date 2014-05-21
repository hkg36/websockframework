//
//  Google Prettify
//  A showdown extension to add Google Prettify (http://code.google.com/p/google-code-prettify/)
//  hints to showdown's HTML output.
//

(function(){

    var prettify = function(converter) {
        return [
            { type: 'output', filter: function(source){

                return source.replace(/<code\s+class="(\w*)">/gi, function(match, cls) {
                    return '<code class="'+cls+' hljs">';
                });
            }}
        ];
    };

    // Client-side export
    if (typeof window !== 'undefined' && window.Showdown && window.Showdown.extensions) { window.Showdown.extensions.prettify = prettify; }
    // Server-side export
    if (typeof module !== 'undefined') module.exports = prettify;

}());
