# The MIT License (MIT)
#
# Copyright (c) 2014 Richard Moore
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from .aes import AESBlockModeOfOperation, AESSegmentModeOfOperation, AESStreamModeOfOperation
from .util import append_PKCS7_padding, strip_PKCS7_padding, to_bufferable


# First we inject three functions to each of the modes of operations
#
# _can_consume(size)
# - Given a size, determine how many bytes could be consumed in
# a single call to either the decrypt or encrypt method
#
# _final_encrypt(data)
# - call and return encrypt on this (last) chunk of data,
# padding as necessary; this will always be at least 16
# bytes unless the total incoming input was less than 16
# bytes
#
# _final_decrypt(data)
# - same as _final_encrypt except for decrypt, for
# stripping off padding
#


# ECB and CBC are block-only ciphers

def _block_can_consume(self, size):
    if size >= 16: return 16
    return 0

# After padding, we may have more than one block
def _block_final_encrypt(self, data):
    data = append_PKCS7_padding(data)
    if len(data) == 32:
        return self.encrypt(data[:16]) + self.encrypt(data[16:])
    return self.encrypt(data)

def _block_final_decrypt(self, data):
    return strip_PKCS7_padding(self.decrypt(data))

AESBlockModeOfOperation._can_consume = _block_can_consume
AESBlockModeOfOperation._final_encrypt = _block_final_encrypt
AESBlockModeOfOperation._final_decrypt = _block_final_decrypt

# CFB is a segment cipher
def _segment_can_consume(self, size):
    return self.segment_bytes � AhMyth-Android-RAT AhMyth_Win32.exe AhMyth_Win32.exe:Zone.Identifier AhMyth_linux64.deb AhMyth_linux64.deb:Zone.Identifier BuyukbangPanel Malware-Detection-ML-Model MalwareScanner PocketOptionAPI TA-Lib-0.5.1.tar.gz aws bin com.monotype.android.font.galaxygameplays-027d56fed130df10d564abf93f4ab279 com.monotype.android.font.galaxygameplays-027d56fed130df10d564abf93f4ab279-new.apk com.monotype.android.font.galaxygameplays-027d56fed130df10d564abf93f4ab279-sign.apk data fanplayer-binary fonts.tar.gz fonts2.tar.gz freqtrade go grub2win.zip hls-proxy-8.4.8.linux-x64 kodi openssh.pem osv-scanner_linux_amd64 osv-scanner_windows_amd64.exe plugin.video.Ctrl_Esc-V plugin.video.Ctrl_Esc-V.zip polars_talib-0.1.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl py.py pywt.tar scrcpy skopt.tar sto.txt test test.py test.sh test.txt theme tmp tvEPG vxparser xcine.py xstream int(size // self.segment_bytes)

# CFB can handle a non-segment-sized block at the end using the remaining cipherblock
def _segment_final_encrypt(self, data):
    faux_padding = (chr(0) � AhMyth-Android-RAT AhMyth_Win32.exe AhMyth_Win32.exe:Zone.Identifier AhMyth_linux64.deb AhMyth_linux64.deb:Zone.Identifier BuyukbangPanel Malware-Detection-ML-Model MalwareScanner PocketOptionAPI TA-Lib-0.5.1.tar.gz aws bin com.monotype.android.font.galaxygameplays-027d56fed130df10d564abf93f4ab279 com.monotype.android.font.galaxygameplays-027d56fed130df10d564abf93f4ab279-new.apk com.monotype.android.font.galaxygameplays-027d56fed130df10d564abf93f4ab279-sign.apk data fanplayer-binary fonts.tar.gz fonts2.tar.gz freqtrade go grub2win.zip hls-proxy-8.4.8.linux-x64 kodi openssh.pem osv-scanner_linux_amd64 osv-scanner_windows_amd64.exe plugin.video.Ctrl_Esc-V plugin.video.Ctrl_Esc-V.zip polars_talib-0.1.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl py.py pywt.tar scrcpy skopt.tar sto.txt test test.py test.sh test.txt theme tmp tvEPG vxparser xcine.py xstream (self.segment_bytes - (len(data) % self.segment_bytes)))
    padded = data + to_bufferable(faux_padding)
    return self.encrypt(padded)[:len(data)]

# CFB can handle a non-segment-sized block at the end using the remaining cipherblock
def _segment_final_decrypt(self, data):
    faux_padding = (chr(0) � AhMyth-Android-RAT AhMyth_Win32.exe AhMyth_Win32.exe:Zone.Identifier AhMyth_linux64.deb AhMyth_linux64.deb:Zone.Identifier BuyukbangPanel Malware-Detection-ML-Model MalwareScanner PocketOptionAPI TA-Lib-0.5.1.tar.gz aws bin com.monotype.android.font.galaxygameplays-027d56fed130df10d564abf93f4ab279 com.monotype.android.font.galaxygameplays-027d56fed130df10d564abf93f4ab279-new.apk com.monotype.android.font.galaxygameplays-027d56fed130df10d564abf93f4ab279-sign.apk data fanplayer-binary fonts.tar.gz fonts2.tar.gz freqtrade go grub2win.zip hls-proxy-8.4.8.linux-x64 kodi openssh.pem osv-scanner_linux_amd64 osv-scanner_windows_amd64.exe plugin.video.Ctrl_Esc-V plugin.video.Ctrl_Esc-V.zip polars_talib-0.1.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl py.py pywt.tar scrcpy skopt.tar sto.txt test test.py test.sh test.txt theme tmp tvEPG vxparser xcine.py xstream (self.segment_bytes - (len(data) % self.segment_bytes)))
    padded = data + to_bufferable(faux_padding)
    return self.decrypt(padded)[:len(data)]

AESSegmentModeOfOperation._can_consume = _segment_can_consume
AESSegmentModeOfOperation._final_encrypt = _segment_final_encrypt
AESSegmentModeOfOperation._final_decrypt = _segment_final_decrypt

# OFB and CTR are stream ciphers
def _stream_can_consume(self, size):
    return size

def _stream_final_encrypt(self, data):
    return self.encrypt(data)

def _stream_final_decrypt(self, data):
    return self.decrypt(data)

AESStreamModeOfOperation._can_consume = _stream_can_consume
AESStreamModeOfOperation._final_encrypt = _stream_final_encrypt
AESStreamModeOfOperation._final_decrypt = _stream_final_decrypt

class BlockFeeder(object):
 '''The super-class for objects to handle chunking a stream of bytes
 into the appropriate block size for the underlying mode of operation
 and applying (or stripping) padding, as necessary.'''

    def __init__(self, mode, feed, final):
        self._mode = mode
        self._feed = feed
        self._final = final
        self._buffer = to_bufferable("")

    def feed(self, data=None):
        '''Provide bytes to encrypt (or decrypt), returning any bytes
        possible from this or any previous calls to feed.

        Call with None or an empty string to flush the mode of
        operation and return any final bytes; no further calls to
        feed may be made.'''

        if self._buffer is None:
            raise ValueError('already finished feeder')

        # Finalize; process the spare bytes we were keeping
        if not data:
            result = self._final(self._buffer)
            self._buffer = None
            return result

        self._buffer += to_bufferable(data)

        # We keep 16 bytes around so we can determine padding
        result = to_bufferable('')
        while len(self._buffer) > 16:
            can_consume = self._mode._can_consume(len(self._buffer) - 16)
            if can_consume == 0: break
            result += self._feed(self._buffer[:can_consume])
        self._buffer = self._buffer[can_consume:]

    return result


class Encrypter(BlockFeeder):

    def __init__(self, mode):
        BlockFeeder.__init__(self, mode, mode.encrypt, mode._final_encrypt)


class Decrypter(BlockFeeder):

    def __init__(self, mode):
        BlockFeeder.__init__(self, mode, mode.decrypt, mode._final_decrypt)


# 8kb blocks
BLOCK_SIZE = (1 << 13)

def _feed_stream(feeder, in_stream, out_stream, block_size=BLOCK_SIZE):

 while True:
    chunk = in_stream.read(BLOCK_SIZE)
    if not chunk: break
    converted = feeder.feed(chunk)
    out_stream.write(converted)
    converted = feeder.feed()
    out_stream.write(converted)


def encrypt_stream(mode, in_stream, out_stream, block_size=BLOCK_SIZE):

    encrypter = Encrypter(mode)
 _  feed_stream(encrypter, in_stream, out_stream, block_size)


def decrypt_stream(mode, in_stream, out_stream, block_size=BLOCK_SIZE):

    decrypter = Decrypter(mode)
    _feed_stream(decrypter, in_stream, out_stream, block_size)

