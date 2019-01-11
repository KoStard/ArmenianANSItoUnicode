from zipfile import ZipFile, ZIP_STORED, ZipInfo
import tempfile
import shutil
import os
import sys
import zipfile
import re
import math
import shutil
mp = {
    '²': 'Ա',
    '³': 'ա',
    '´': 'Բ',
    'µ': 'բ',
    'μ': 'բ',
    '¶': 'Գ',
    '·': 'գ',
    '¸': 'Դ',
    '¹': 'դ',
    'º': 'Ե',
    '»': 'ե',
    '¼': 'Զ',
    '½': 'զ',
    '¾': 'Է',
    '¿': 'է',
    'À': 'Ը',
    'Á': 'ը',
    'Â': 'Թ',
    'Ã': 'թ',
    'Ä': 'Ժ',
    'Å': 'ժ',
    'Æ': 'Ի',
    'Ç': 'ի',
    'È': 'Լ',
    'É': 'լ',
    'Ê': 'Խ',
    'Ë': 'խ',
    'Ì': 'Ծ',
    'Í': 'ծ',
    'Î': 'Կ',
    'Ï': 'կ',
    'Ð': 'Հ',
    'Ñ': 'հ',
    'Ò': 'Ձ',
    'Ó': 'ձ',
    'Ô': 'Ղ',
    'Õ': 'ղ',
    'Ö': 'Ճ',
    '×': 'ճ',
    'Ø': 'Մ',
    'Ù': 'մ',
    'Ú': 'Յ',
    'Û': 'յ',
    'Ü': 'Ն',
    'Ý': 'ն',
    'Þ': 'Շ',
    'ß': 'շ',
    'à': 'Ո',
    'á': 'ո',
    'â': 'Չ',
    'ã': 'չ',
    'ä': 'Պ',
    'å': 'պ',
    'æ': 'Ջ',
    'ç': 'ջ',
    'è': 'Ռ',
    'é': 'ռ',
    'ê': 'Ս',
    'ë': 'ս',
    'ì': 'Վ',
    'í': 'վ',
    'î': 'Տ',
    'ï': 'տ',
    'ð': 'Ր',
    'ñ': 'ր',
    'ò': 'Ց',
    'ó': 'ց',
    'ô': 'Ւ',
    'õ': 'ւ',
    'ö': 'Փ',
    '÷': 'փ',
    'ø': 'Ք',
    'ù': 'ք',
    'ú': 'Օ',
    'û': 'օ',
    'ü': 'Ֆ',
    'ý': 'ֆ',
    '¨': 'և',
    '·': '•',
    '•': 'գ',
    '\'': '՚',
    '°': '՛',
    '¯': '՜',
    'ª': '՝',
    '±': '՞',
    '£': '։',
    '§': '«',
    '¦': '»',
    '«': ',',
    '©': '.',
    '®': '…'
}

bmp = {
    b'\xc2\xb2': b'\xd4\xb1',
    b'\xc2\xb3': b'\xd5\xa1',
    b'\xc2\xb4': b'\xd4\xb2',
    b'\xc2\xb5': b'\xd5\xa2',
    b'\xce\xbc': b'\xd5\xa2',
    b'\xc2\xb6': b'\xd4\xb3',
    b'\xc2\xb7': b'\xd5\xa3',
    b'\xc2\xb8': b'\xd4\xb4',
    b'\xc2\xb9': b'\xd5\xa4',
    b'\xc2\xba': b'\xd4\xb5',
    b'\xc2\xbb': b'\xd5\xa5',
    b'\xc2\xbc': b'\xd4\xb6',
    b'\xc2\xbd': b'\xd5\xa6',
    b'\xc2\xbe': b'\xd4\xb7',
    b'\xc2\xbf': b'\xd5\xa7',
    b'\xc3\x80': b'\xd4\xb8',
    b'\xc3\x81': b'\xd5\xa8',
    b'\xc3\x82': b'\xd4\xb9',
    b'\xc3\x83': b'\xd5\xa9',
    b'\xc3\x84': b'\xd4\xba',
    b'\xc3\x85': b'\xd5\xaa',
    b'\xc3\x86': b'\xd4\xbb',
    b'\xc3\x87': b'\xd5\xab',
    b'\xc3\x88': b'\xd4\xbc',
    b'\xc3\x89': b'\xd5\xac',
    b'\xc3\x8a': b'\xd4\xbd',
    b'\xc3\x8b': b'\xd5\xad',
    b'\xc3\x8c': b'\xd4\xbe',
    b'\xc3\x8d': b'\xd5\xae',
    b'\xc3\x8e': b'\xd4\xbf',
    b'\xc3\x8f': b'\xd5\xaf',
    b'\xc3\x90': b'\xd5\x80',
    b'\xc3\x91': b'\xd5\xb0',
    b'\xc3\x92': b'\xd5\x81',
    b'\xc3\x93': b'\xd5\xb1',
    b'\xc3\x94': b'\xd5\x82',
    b'\xc3\x95': b'\xd5\xb2',
    b'\xc3\x96': b'\xd5\x83',
    b'\xc3\x97': b'\xd5\xb3',
    b'\xc3\x98': b'\xd5\x84',
    b'\xc3\x99': b'\xd5\xb4',
    b'\xc3\x9a': b'\xd5\x85',
    b'\xc3\x9b': b'\xd5\xb5',
    b'\xc3\x9c': b'\xd5\x86',
    b'\xc3\x9d': b'\xd5\xb6',
    b'\xc3\x9e': b'\xd5\x87',
    b'\xc3\x9f': b'\xd5\xb7',
    b'\xc3\xa0': b'\xd5\x88',
    b'\xc3\xa1': b'\xd5\xb8',

    b'\xc3\xa2': b'\xd5\x89',
    b'\xc3\xa3': b'\xd5\xb9',
    b'\xc3\xa4': b'\xd5\x8a',
    b'\xc3\xa5': b'\xd5\xba',
    b'\xc3\xa6': b'\xd5\x8b',
    b'\xc3\xa7': b'\xd5\xbb',
    b'\xc3\xa8': b'\xd5\x8c',
    b'\xc3\xa9': b'\xd5\xbc',
    b'\xc3\xaa': b'\xd5\x8d',
    b'\xc3\xab': b'\xd5\xbd',
    b'\xc3\xac': b'\xd5\x8e',
    b'\xc3\xad': b'\xd5\xbe',
    b'\xc3\xae': b'\xd5\x8f',
    b'\xc3\xaf': b'\xd5\xbf',
    b'\xc3\xb0': b'\xd5\x90',

    b'\xc3\xb1': b'\xd6\x80',
    b'\xc3\xb2': b'\xd5\x91',
    b'\xc3\xb3': b'\xd6\x81',
    b'\xc3\xb4': b'\xd5\x92',
    b'\xc3\xb5': b'\xd6\x82',
    b'\xc3\xb6': b'\xd5\x93',
    b'\xc3\xb7': b'\xd6\x83',

    b'\xc3\xb8': b'\xd5\x94',
    b'\xc3\xb9': b'\xd6\x84',
    b'\xc3\xba': b'\xd5\x95',
    b'\xc3\xbb': b'\xd6\x85',

    b'\xc3\xbc': b'\xd5\x96',
    b'\xc3\xbd': b'\xd6\x86',

    b'\xc2\xa8': b'\xd6\x87',
    # b'\xc2\xb7': b'\xe2\x80',

    # b'\xe2\x80': b'\xa2<',
    # b'\xa2<': b'\xd5\xa3',
    # b"'<": b'\xd5\x9a',

    b'\xc2\xb0': b'\xd5\x9b',
    b'\xc2\xaf': b'\xd5\x9c',
    b'\xc2\xaa': b'\xd5\x9d',
    b'\xc2\xb1': b'\xd5\x9e',
    b'\xc2\xa3': b'\xd6\x89',
    b'\xc2\xa7': b'\xc2\xab',
    b'\xc2\xa6': b'\xc2\xbb',
    # b'\xc2\xab': b',<',
    # b'\xc2\xa9': b'.<',
    # b'\xc2\xae': b"'<",
}


def get_unique_name(filename):
    dirname = os.path.dirname(filename)
    filename = filename[len(dirname) + (1 if dirname else 0):]
    content = os.listdir(dirname or None)
    if filename in content:
        if '.' in filename:
            name = '.'.join(filename.split('.')[:-1])
            ext = filename[len(name) + (1 if name else 0):]
        else:
            name = filename
            ext = ''
        i = 1
        while '{}-{}.{}'.format(name, i, ext) in content:
            i += 1
        return dirname+'{}-{}.{}'.format(name, i, ext)
    else:
        return dirname+filename


def get_output_filename(filename):
    dirname = os.path.dirname(filename)
    filename = filename[len(dirname) + (1 if dirname else 0):]
    if '.' in filename:
        name = '.'.join(filename.split('.')[:-1])
        ext = filename[len(name) + (1 if name else 0):]
    else:
        name = filename
        ext = ''
    name += '-output'
    return get_unique_name(dirname+'{}.{}'.format(name, ext))


class UpdateableZipFile(ZipFile):
    """
    Add delete (via remove_file) and update (via writestr and write methods)
    To enable update features use UpdateableZipFile with the 'with statement',
    Upon  __exit__ (if updates were applied) a new zip file will override the exiting one with the updates
    """

    class DeleteMarker(object):
        pass

    def __init__(self, file, mode="r", compression=ZIP_STORED, allowZip64=False):
        # Init base
        super(UpdateableZipFile, self).__init__(file, mode=mode,
                                                compression=compression,
                                                allowZip64=allowZip64)
        # track file to override in zip
        self._replace = {}
        # Whether the with statement was called
        self._allow_updates = False

    def writestr(self, zinfo_or_arcname, bytes, compress_type=None):
        if isinstance(zinfo_or_arcname, ZipInfo):
            name = zinfo_or_arcname.filename
        else:
            name = zinfo_or_arcname
        # If the file exits, and needs to be overridden,
        # mark the entry, and create a temp-file for it
        # we allow this only if the with statement is used
        if self._allow_updates and name in self.namelist():
            temp_file = self._replace[name] = self._replace.get(name,
                                                                tempfile.TemporaryFile())
            temp_file.write(bytes)
        # Otherwise just act normally
        else:
            super(UpdateableZipFile, self).writestr(zinfo_or_arcname,
                                                    bytes, compress_type=compress_type)

    def write(self, filename, arcname=None, compress_type=None):
        arcname = arcname or filename
        # If the file exits, and needs to be overridden,
        # mark the entry, and create a temp-file for it
        # we allow this only if the with statement is used
        if self._allow_updates and arcname in self.namelist():
            temp_file = self._replace[arcname] = self._replace.get(arcname,
                                                                   tempfile.TemporaryFile())
            with open(filename, "rb") as source:
                shutil.copyfileobj(source, temp_file)
        # Otherwise just act normally
        else:
            super(UpdateableZipFile, self).write(filename,
                                                 arcname=arcname, compress_type=compress_type)

    def __enter__(self):
        # Allow updates
        self._allow_updates = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # call base to close zip file, organically
        try:
            super(UpdateableZipFile, self).__exit__(exc_type, exc_val, exc_tb)
            if len(self._replace) > 0:
                self._rebuild_zip()
        finally:
            # In case rebuild zip failed,
            # be sure to still release all the temp files
            self._close_all_temp_files()
            self._allow_updates = False

    def _close_all_temp_files(self):
        for temp_file in self._replace.values():
            if hasattr(temp_file, 'close'):
                temp_file.close()

    def remove_file(self, path):
        self._replace[path] = self.DeleteMarker()

    def _rebuild_zip(self):
        tempdir = tempfile.mkdtemp()
        try:
            temp_zip_path = os.path.join(tempdir, 'new.zip')
            with ZipFile(self.filename, 'r') as zip_read:
                # Create new zip with assigned properties
                with ZipFile(temp_zip_path, 'w', compression=self.compression,
                             allowZip64=self._allowZip64) as zip_write:
                    for item in zip_read.infolist():
                        # Check if the file should be replaced / or deleted
                        replacement = self._replace.get(item.filename, None)
                        # If marked for deletion, do not copy file to new zipfile
                        if isinstance(replacement, self.DeleteMarker):
                            del self._replace[item.filename]
                            continue
                        # If marked for replacement, copy temp_file, instead of old file
                        elif replacement is not None:
                            del self._replace[item.filename]
                            # Write replacement to archive,
                            # and then close it (deleting the temp file)
                            replacement.seek(0)
                            data = replacement.read()
                            replacement.close()
                        else:
                            data = zip_read.read(item.filename)
                        zip_write.writestr(item, data)
            # Override the archive with the updated one
            shutil.move(temp_zip_path, self.filename)
        finally:
            shutil.rmtree(tempdir)


def convert_data(data, ops, cls):
    perc = 0
    lastRound = 0
    for i in range(len(ops)):  # len(ops)
        perc = (i+1)*100 / len(ops)
        if math.floor(perc) // 10 > lastRound:
            lastRound = math.floor(perc) // 10
            print("{}%".format(math.floor(perc)))
        buffer = bytearray()
        res = bytearray()
        for j in range(ops[i], cls[i]):
            buffer += data[j:j+1]
            if j == ops[i]:
                continue
            if bytes(buffer) in bmp:
                res += bmp[bytes(buffer)]
                buffer.clear()
            else:
                if len(buffer) >= 2:
                    res += buffer[:-1]
                    buffer = buffer[-1:]
        res += buffer
        data[ops[i]: cls[i]] = res


def processDocx(filename):
    """ Converting data from innerText of w:t tags """
    zfile = zipfile.ZipFile(filename, 'r')
    data = bytearray(zfile.open('word/document.xml').read())
    zfile.close()

    op = re.compile(b'<w:t(?: [^>]*|)>')
    cl = re.compile(b'</w:t>')

    ops = [x.end() for x in op.finditer(data)]
    cls = [x.start() for x in cl.finditer(data)]
    convert_data(data, ops, cls)

    print("Saving...")
    new_filename = get_output_filename(filename)
    print("Saving to: {}".format(new_filename))
    shutil.copyfile(filename, new_filename)
    with UpdateableZipFile(new_filename, 'a') as f:
        f.writestr('word/document.xml', data)
    print("Done")


def processPDF(filename):
    print("Can't do anything yet...")


def processTXT(filename):
    data = bytearray(open(filename, 'rb').read())
    convert_data(data, [0], [len(data)])
    print("Saving...")
    open(get_output_filename(filename), 'wb').write(data)
    print("Done")


filename = ''
if len(sys.argv) > 1:
    filename = sys.argv[1]
while not filename:
    fn = input("Please input valid docx filename: ")

ext = filename.split('.')[-1]
if ext == 'docx':
    processDocx(filename)
elif ext == 'pdf':
    processPDF(filename)
elif ext == 'txt':
    processTXT(filename)
else:
    print("Invalid file type {}".format(ext))
