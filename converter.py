from universals import as_daemon
from zipfile import ZipFile, ZIP_STORED, ZipInfo
import tempfile
import os
import sys
import zipfile
import re
import subprocess
import shutil
from ANSIDecoder import decode_data


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
        return dirname + ('/' if dirname else '') + '{}-{}.{}'.format(
            name, i, ext)
    else:
        return dirname + ('/' if dirname else '') + filename


def get_output_filename(filename):
    dirname = os.path.dirname(filename)
    filename = filename[len(dirname) + (1 if dirname else 0):]
    if '.' in filename:
        name = '.'.join(filename.split('.')[:-1])
        ext = filename[len(name) + (1 if name else 0):]
    else:
        name = filename
        ext = ''
    name += '-converted'
    return get_unique_name(dirname + ('/' if dirname else '') +
                           '{}.{}'.format(name, ext))


class UpdateableZipFile(ZipFile):
    """
    Add delete (via remove_file) and update (via writestr and write methods)
    To enable update features use UpdateableZipFile with the 'with statement',
    Upon  __exit__ (if updates were applied) a new zip file will override the exiting one with the updates
    """

    class DeleteMarker(object):
        pass

    def __init__(self,
                 file,
                 mode="r",
                 compression=ZIP_STORED,
                 allowZip64=False):
        # Init base
        super(UpdateableZipFile, self).__init__(
            file, mode=mode, compression=compression, allowZip64=allowZip64)
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
            temp_file = self._replace[name] = self._replace.get(
                name, tempfile.TemporaryFile())
            temp_file.write(bytes)
        # Otherwise just act normally
        else:
            super(UpdateableZipFile, self).writestr(
                zinfo_or_arcname, bytes, compress_type=compress_type)

    def write(self, filename, arcname=None, compress_type=None):
        arcname = arcname or filename
        # If the file exits, and needs to be overridden,
        # mark the entry, and create a temp-file for it
        # we allow this only if the with statement is used
        if self._allow_updates and arcname in self.namelist():
            temp_file = self._replace[arcname] = self._replace.get(
                arcname, tempfile.TemporaryFile())
            with open(filename, "rb") as source:
                shutil.copyfileobj(source, temp_file)
        # Otherwise just act normally
        else:
            super(UpdateableZipFile, self).write(
                filename, arcname=arcname, compress_type=compress_type)

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
                with ZipFile(
                        temp_zip_path,
                        'w',
                        compression=self.compression,
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


def processDocx(filename, handler=None, handler_getter=None):
    """ Converting data from innerText of w:t tags """
    zfile = zipfile.ZipFile(filename, 'r')
    data = bytearray(zfile.open('word/document.xml').read())
    zfile.close()

    op = re.compile(b'<w:t(?: [^>]*|)>')
    cl = re.compile(b'</w:t>')

    ops = [x.end() for x in op.finditer(data)]
    cls = [x.start() for x in cl.finditer(data)]
    decode_data(data, ops, cls, handler=handler, handler_getter=handler_getter)

    print("Saving...")
    new_filename = get_output_filename(filename)
    print("Saving to: {}".format(new_filename))
    shutil.copyfile(filename, new_filename)
    with UpdateableZipFile(new_filename, 'a') as f:
        f.writestr('word/document.xml', data)
    print("Done")
    return new_filename


def processPPTX(filename, handler=None, handler_getter=None):
    """ Converting data from innerText of w:t tags """
    zfile = zipfile.ZipFile(filename, 'r')
    data = []
    slides_number = 0
    for fn in zfile.namelist():
        m = re.match('ppt/slides/slide(\d+)\.xml', fn)
        if m:
            index = int(m.group(1))
            if index > slides_number:
                slides_number = index
    for slide_index in range(1, slides_number):
        slide_data = bytearray(
            zfile.open('ppt/slides/slide{}.xml'.format(slide_index)).read())

        op = re.compile(b'<a:t(?: [^>]*|)>')
        cl = re.compile(b'</a:t>')

        ops = [x.end() for x in op.finditer(slide_data)]
        cls = [x.start() for x in cl.finditer(slide_data)]
        decode_data(
            slide_data,
            ops,
            cls,
            handler=handler,
            handler_getter = handler_getter,
            perc_from=(slide_index - 1) * 90 // (slides_number - 1),
            perc_to=slide_index * 90 //
            (slides_number - 1))  # Will result to blinking progress bar
        data.append(slide_data)

    zfile.close()
    print("Saving...")
    new_filename = get_output_filename(filename)
    print("Saving to: {}".format(new_filename))
    shutil.copyfile(filename, new_filename)
    with UpdateableZipFile(new_filename, 'a') as f:
        for i in range(len(data)):
            f.writestr('ppt/slides/slide{}.xml'.format(i + 1), data[i])
    print("Done")
    return new_filename


def processTXT(filename, handler=None, handler_getter=None):
    data = bytearray(open(filename, 'rb').read())
    decode_data(data, [0], [len(data)], handler=handler, handler_getter=handler_getter)
    new_filename = get_output_filename(filename)
    print("Saving...")
    open(new_filename, 'wb').write(data)
    print("Done")
    return new_filename

def process_doc(filename, handler=None, handler_getter=None):
    """
    Will process .doc files in platform specific manner
     - For the linux will use soffice
     - For the windows will use win32com.client
    """
    if sys.platform == 'linux':
        subprocess.call(['soffice', '--headless', '--convert-to', 'docx', filename])
        new_filename = re.sub(r'\.\w+$', '.docx', os.path.split(filename)[1])
        converted_filename = processDocx(new_filename, handler)
        os.remove(new_filename)
        moved_converted_filename = os.path.split(filename)[0]+os.path.split(converted_filename)[1]
        os.rename(converted_filename, moved_converted_filename)
        return moved_converted_filename
    elif sys.platform == 'win32':
        import win32com.client as win32
        from win32com.client import constants

        # Opening MS Word
        word = win32.gencache.EnsureDispatch('Word.Application')
        doc = word.Documents.Open(filename)
        doc.Activate()

        # Rename path with .docx
        new_file_abs = os.path.abspath(filename)
        new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

        # Save and Close
        word.ActiveDocument.SaveAs(
            new_file_abs, FileFormat=constants.wdFormatXMLDocument
        )
        doc.Close(False)
        return processDocx(new_file_abs, handler)
    else:
        raise NotImplementedError("Not implemented for current platform!")

available_formats = {
    'docx': processDocx,
    'pptx': processPPTX,
    'txt': processTXT
}

if sys.platform in ('linux', 'win32'):
    available_formats['doc'] = process_doc


def process(filename, *, handler=None, handler_getter=None, files_status_handler=None):
    ext = os.path.splitext(filename)[1][1:]
    if ext not in available_formats:
        print("Invalid format")
        return
    new_filename = available_formats[ext](filename, handler, handler_getter=handler_getter)
    if handler:
        handler.setValue(100)
    if handler_getter:
        handler_getter().setValue(100)
    if files_status_handler:
        files_status_handler[filename] = new_filename
    return new_filename


if __name__ == '__main__':
    filename = ''
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    while not filename:
        fn = input("Please input valid docx filename: ")

    ext = filename.split('.')[-1]
    if ext in available_formats:
        available_formats[ext](filename)
    else:
        print("Invalid file type {}".format(ext))
