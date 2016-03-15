"""
A unified interface to builtin hashers and codecs as well as some of my own.
NOTE: The PD series is experimental, and is not considered very secure.

AUTHORS:
v1.2.0+             --> pydsigner
"""

import hashlib
import base64
import zlib
import binascii
try:
    import urllib.parse as urler
except ImportError:
    import urllib as urler

from . import iter_utils


__all__ = ['fetcher', 'Triplets', 'SHA1', 'SHA224', 'SHA256', 'SHA384',
           'SHA512', 'MD5', 'Base16', 'Base32', 'Base64', 'Hex', 'HQX', 'UU',
           'URL', 'HTML', 'CRC32', 'Adler32']


class Triplets(object):
    """
    A toy cipher.
    
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return '.'.join([str(ord(c) * 3) for c in s])
    def decode(self, s):
        return ''.join([chr(int(c) // 3) for c in s.split('.')])


class SHA1(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return hashlib.sha1(s).hexdigest()


class SHA224(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return hashlib.sha224(s).hexdigest()


class SHA256(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return hashlib.sha256(s).hexdigest()


class SHA384(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return hashlib.sha384(s).hexdigest()


class SHA512(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return hashlib.sha512(s).hexdigest()


class MD5(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return hashlib.md5(s).hexdigest()


class Base16(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return base64.b16encode(s)
    def decode(self, s):
        return base64.b16decode(s)


class Base32(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return base64.b32encode(s)
    def decode(self, s):
        return base64.b32decode(s)


class Base64(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return base64.b64encode(s)
    def decode(self, s):
        return base64.b64decode(s)


class Hex(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return binascii.b2a_hex(s)
    def decode(self, s):
        return binascii.a2b_hex(s)


class HQX(object):
    
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return binascii.b2a_hqx(s)
    def decode(self, s):
        return binascii.a2b_hqx(s)[0]


class UU(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return binascii.b2a_uu(s)
    def decode(self, s):
        return binascii.a2b_uu(s)


class URL(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    def encode(self, s):
        return urler.quote(s)
    def decode(self, s):
        return urler.unquote(s)


class HTML(object):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    
    conv_dict = {'<': '&#60;', '>': '&#62;', '"': '&#34;', '&': '&#38;'}
    
    def encode(self, s):
        return iter_utils.many(s, self.conv_dict)
    def decode(self, s):
        return iter_utils.many(s, self.conv_dict, True)


class CRC32(object):
    """
    AUTHORS:
    v0.2.7+             --> pydsigner
    """
    
    def encode(self, s):
        return zlib.crc32(s)


class Adler32(object):
    """AUTHORS:
    v0.2.7+             --> pydsigner
    """
    
    def encode(self, s):
        return zlib.adler32(s)


encoder_classes = dict(triplets=Triplets, sha1=SHA1, sha224=SHA224,
                       sha256=SHA256, sha384=SHA384, sha512=SHA512, md5=MD5, 
                       base16=Base16, base32=Base32, base64=Base64, hex=Hex, 
                       hqx=HQX, uu=UU, url=URL, html=HTML, crc32=CRC32, 
                       adler32=Adler32)


def fetcher(encoder):
    """
    AUTHORS:
    v0.2.0+             --> pydsigner
    """
    return encoder_classes[encoder.lower()]()
