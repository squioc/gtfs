from csv import DictReader
import codecs

class UTF8Encoder(object):
    def __init__(self, reader):
        self.reader = codecs.getreader("utf-8")(reader)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class CSVUnicodeReader(object):
    def __init__(self, stream):
        self.reader = DictReader(UTF8Encoder(stream))

    def __iter__(self):
        return self

    def next(self):
        entry = self.reader.next()
        return dict([(unicode(k, "utf-8"), unicode(v, "utf-8")) for (k,v) in entry.items()])

