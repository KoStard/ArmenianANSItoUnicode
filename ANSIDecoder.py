import math

# mp = {'²': 'Ա','³': 'ա','´': 'Բ','µ': 'բ','μ': 'բ','¶': 'Գ','·': 'գ','¸': 'Դ','¹': 'դ','º': 'Ե','»': 'ե','¼': 'Զ','½': 'զ','¾': 'Է','¿': 'է','À': 'Ը','Á': 'ը','Â': 'Թ','Ã': 'թ','Ä': 'Ժ','Å': 'ժ','Æ': 'Ի','Ç': 'ի','È': 'Լ','É': 'լ','Ê': 'Խ','Ë': 'խ','Ì': 'Ծ','Í': 'ծ','Î': 'Կ','Ï': 'կ','Ð': 'Հ','Ñ': 'հ','Ò': 'Ձ','Ó': 'ձ','Ô': 'Ղ','Õ': 'ղ','Ö': 'Ճ','×': 'ճ','Ø': 'Մ','Ù': 'մ','Ú': 'Յ','Û': 'յ','Ü': 'Ն','Ý': 'ն','Þ': 'Շ','ß': 'շ','à': 'Ո','á': 'ո','â': 'Չ','ã': 'չ','ä': 'Պ','å': 'պ','æ': 'Ջ','ç': 'ջ','è': 'Ռ','é': 'ռ','ê': 'Ս','ë': 'ս','ì': 'Վ','í': 'վ','î': 'Տ','ï': 'տ','ð': 'Ր','ñ': 'ր','ò': 'Ց','ó': 'ց','ô': 'Ւ','õ': 'ւ','ö': 'Փ','÷': 'փ','ø': 'Ք','ù': 'ք','ú': 'Օ','û': 'օ','ü': 'Ֆ','ý': 'ֆ','¨': 'և','·': '•','•': 'գ','\'': '՚','°': '՛','¯': '՜','ª': '՝','±': '՞','£': '։','§': '«','¦': '»','«': ',','©': '.','®': '…'}

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


def decode_data(data, ops=None, cls=None, *, silent=True, decode=False):
    """ Will decode ANSI Armenian characters and convert them to UTF-8 """
    if isinstance(data, str):
        data = bytearray(data, 'utf-8')
    perc = 0
    lastRound = 0
    if not ops:
        ops = [0]
    if not cls:
        cls = [len(data)]
    for i in range(len(ops)):  # len(ops)
        if not silent:
            perc = (i + 1) * 100 / len(ops)
            if math.floor(perc) // 10 > lastRound:
                lastRound = math.floor(perc) // 10
                print("{}%".format(math.floor(perc)))
        buffer = bytearray()
        res = bytearray()
        for j in range(ops[i], cls[i]):
            buffer += data[j:j + 1]
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
        data[ops[i]:cls[i]] = res
    return data if not decode else data.decode('utf-8')
