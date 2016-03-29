# coding=utf-8
#

class BookReps():
    reps = [
        {
            'find': ' xmlns:i18n="http://apache.org/cocoon/i18n/2.1"',
            'rep': ''
        },
        {
            'find': u' xmlns:str="http://exslt.org/strings"',
            'rep': u''
        },
        {
            'find': u'&nbsp;',
            'rep': u' '
        },
        {
            'find': u'&lsquo;',
            'rep': u'‘'
        },
        {
            'find': u'&rsquo;',
            'rep': u'’'
        },
        {
            'find': u'&ldquo;',
            'rep': u'“'
        },
        {
            'find': u'&rdquo;',
            'rep': u'”'
        },
        {
            'regex': True,
            'find': u'!book=/***BKNAME***/wb/[\w\-]+/"\s+onmousedown="javascript: \s*document.cookie=&quot;' \
                    u'THLanchor=([\w\-]+);\s+path=/&quot;;',
            'rep': r'\1'
        },
        {
            'regex': True,
            'find': u'<br[^>]*>',
            'rep': r'<br />',
        },
        {
            'regex': True,
            'find': u'<input[^>]*>',
            'rep': r''
        },
        {
            'regex': True,
            'find': u'<img([^>]+)>',
            'rep': r'<img\1 />',
        },
        {
            'regex': True,
            'find': u'<h2 class="h1" id="([^"]+)"><span class="tib">([^<]+)</span></h2>',
            'rep': r'<h1 id="\1"><span class="tib">\2</span></h1>',
        }
    ]

    def getreps(self):
        return self.reps

