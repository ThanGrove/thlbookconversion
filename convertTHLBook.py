# coding=utf-8
#
#  Removes line returns from originals of the proofed volucmes
#

import codecs
from os.path import *
from os import makedirs
from BookReps import *
import re
from lxml import etree

def xmlprint(el):
    print etree.tostring(el, encoding="UTF-8")

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

    def clean(self, bkname):
        if self.mytext:
            c = 0
            for rep in self.replacements:
                c += 1
                if 'regex' in rep and rep['regex']:
                    myfind = rep['find'].replace('***BKNAME***', bkname)
                    self.mytext = re.sub(myfind, rep['rep'], self.mytext)
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
        xfile = codecs.open(outurl, "w")
        xfile.write(self.mytext)
        xfile.close()

    def convertHTML(self):
        '''
        Converts the existing HTML into importable form
        :return: none
        '''
        #tree = etree.parse(self.myurl)
        #print tree
        # Parse existing html into etree
        htmlparser = etree.HTMLParser(encoding="UTF-8")
        htmlparser.feed(self.mytext)
        tree = htmlparser.close()
        # Combine verse Divs
        div = tree.xpath("//div[contains(@class,'verse') and contains(@class,'firstlg')]")
        if div:
            div = div[0]
            # Remove empty <span class="tib"> tags
            rmspans = []
            for c in div.iter():
                ctxt = c.text
                if ctxt:
                    ctxt = ctxt.strip(" \n")
                    if c.tag == "span" and c.get("class") == "tib" and not ctxt:
                        rmspans.append(c)
            for c in rmspans:
                div.remove(c)
            ct = 0
            subdivs = []
            # iterate div siblings to find sister verse divs that are not first lines
            for sib in div.itersiblings("div"):
                ct += 1
                sibclass = sib.get("class")
                if sibclass and "verse" in sibclass and "firstlg" not in sibclass:
                    subdivs.append(sib)
                # Once a div without a verse or a firsclass verse div is found stop iterating siblings
                if "firstclass" in sibclass or "verse" not in sibclass:
                    break
            # add the paragraphs from the related verse divs to this div
            for sd in subdivs:
                p = sd.find("p")
                parentp = div.find("p")
                parentp.append(etree.Element("br"))
                parentp.append(p[0]) # add the span within the p to the p inside the div
                sd.getparent().remove(sd)
        # End combine verse divs

        # Remove page ref anchors
        anchors = tree.xpath("//a[@class='jqmPageRef']")
        for anchor in anchors:
            apar = anchor.getparent()
            apar.text = anchor.text
            apar[0] = anchor[0]
            etree.strip_elements(apar, 'a')

        # Remove all empty span class = tib
        tibspans = tree.xpath('//span[@class="tib"]')
        rmspans = []
        for span in tibspans:
            if len(span) == 0:
                mycnt = span.text
                mycnt = "".join(mycnt.split())
                if not mycnt:
                    rmspans.append(span)

        for span in rmspans:
            par = span.getparent()
            par.remove(span)

        self.mytext = etree.tostring(tree, encoding='UTF-8')


if __name__ == "__main__":

    basepath = "/Users/thangrove/Documents/Project_Data/THL/THL Books/"
    bkname = 'bellezza2'
    txtfile = bkname + "-all"
    turl = basepath + txtfile + "-orig.html"
    tout = basepath + txtfile + "-new2.html"

    book = CleanTHLBook(turl)
    book.clean(bkname)
    book.convertHTML()
    book.writetext(tout)
    print "done!"