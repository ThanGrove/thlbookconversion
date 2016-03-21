# coding=utf-8
#
#  Removes line returns from originals of the proofed volucmes
#

import codecs
from os.path import *
from os import makedirs
from BookReps import *
import re

class CleanTHLBook():

    def __init__(self, url=None):
        self.myurl = None
        self.mytext = None
        if url:
            print "url given is: {0}".format(url)
            print "reading..."
            self.read_doc(url)
        else:
            print "no url!"

        self.replacements = BookReps().getreps()

    def clean(self):
        if self.mytext:
            c = 0
            for rep in self.replacements:
                c += 1
                if 'regex' in rep and rep['regex']:
                    self.mytext = re.sub(rep['find'], rep['rep'], self.mytext)
                else:
                    self.mytext = self.mytext.replace(rep['find'], rep['rep'])
            print "{0} replacements made".format(c)
            for src in re.findall(r'<img[^>]+src="([^"]+)"', self.mytext):
                print "Image: {0}".format(src)

    def read_doc(self, url):
        """Reads in a document from the given local url"""
        self.myurl = url
        try:
            with codecs.open(self.myurl, 'r', encoding='utf-8') as in_stream:
                self.mytext = in_stream.read()

        except UnicodeDecodeError:
            try:
                with codecs.open(self.myurl, 'r', encoding='utf-16') as in_stream:
                    self.mytext = in_stream.read()

            except UnicodeDecodeError:
                print "Unable to open volume file as either utf8 or utf16"


    def writetext(self, outurl=None):
        """Writes just source text to a file regardless on the value of is_xml

        Args:
            outurl (string): the path and name of the outfile

        """
        outurl = outurl if outurl else self.myurl
        xfile = codecs.open(outurl, "w", "utf-8")
        xfile.write(self.mytext)
        xfile.close()


if __name__ == "__main__":

    basepath = "/Users/thangrove/Documents/Project_Data/THL/THL Books/"
    txtfile = "lha-sa-gnas-yig-all"

    turl = basepath + txtfile + "-orig.html"
    tout = basepath + txtfile + "-new.html"
    book = CleanTHLBook(turl)
    book.clean()
    book.writetext(tout)
    print "done!"