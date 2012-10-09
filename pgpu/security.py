'''
A unified interface to builtin hashers and codecs as well as some of my own.

AUTHORS:
v0.2.0+             --> pydsigner
'''

import hashlib
import base64
import zlib
import binascii
import random
import math
import time
import decimal
from decimal import Decimal as dec
import string
try:
    import urllib.parse as urler
except ImportError:
    import urllib as urler

from . import iter_utils
from .compatibility import str, range, chr
from .math_utils import sane_hex


__all__ = ['rand_key', 'multi_pass', 'encoder_classes', 'fetcher', 'Triplets', 
           'PD2', 'PD3', 'PD4', 'PD5', 'PD6', 'PD7', 'PD8', 'PD9', 'PD10', 
           'PD11', 'PD12', 'PD13', 'PD14', 'RD', 'SHA1', 'SHA224', 'SHA256', 
           'SHA384', 'SHA512', 'MD5', 'Base16', 'Base32', 'Base64', 'Hex', 
           'HQX', 'UU', 'URL', 'HTML', 'CRC32', 'Adler32']


class Triplets(object):
    '''
    An encoder useful mostly for minor ciphers or sending information in a 
    format using a small amount of different characters.
    
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return '.'.join([str(ord(c) * 3) for c in s])
    def decode(self, s):
        return ''.join([chr(int(c) // 3) for c in s.split('.')])


class PD2(object):
    '''
    A basic hasher based on PD1(), but with many improvements. This is only 
    recommended for checksums: for passwords, PD6 or a more common hasher 
    should be used.
    
    AUTHORS:
    v0.2.4+             --> pydsigner
    '''
    mag_num = dec('8.33')
    max_len = 30
    
    def encode(self, s):
        L = int(len(s) * self.mag_num)
        res = [str(ord(c) * L) for c in s]
        return ''.join(res)[:self.max_len]


class PD3(object):
    '''
    A more advanced hasher based on PD2(). Should be suitable for passwords, 
    as well as checksums, especially as it is a new hasher. NOTE: This is slow!
    
    AUTHORS:
    v0.2.6+             --> pydsigner
    '''
    decimal.getcontext().prec = 15
    mag_num = dec(5 ** 2 + 9 ** 2).sqrt().rotate(6)
    max_len = 64
    
    def encode(self, s):
        L = int(dec(len(s)) * self.mag_num)
        res = [str(ord(c) * L) for c in s]
        # how slow will this make this hasher?
        decimal.getcontext().prec = 77
        d = dec(''.join(res)).rotate(-1)
        return sane_hex(d)[:self.max_len]


class PD4(object):
    '''
    A more advanced hasher based on PD3(). Should be suitable for passwords, 
    but you may wish to look at PD5(), PD7(), or PD8() for checksums. 
    NOTE: This is VERY slow!
    
    AUTHORS:
    v0.2.9+             --> pydsigner
    '''
    decimal.getcontext().prec = 15
    mag_num = dec(6 ** 2 + 1).sqrt().rotate(-9)
    max_len = 96
    
    def encode(self, s):
        L = int(dec(len(s)) * self.mag_num)
        res = ''.join([str(hash(c) * L) for c in s]).replace('-', '56')
        # Is speed going to be a problem here?
        decimal.getcontext().prec = 116
        d = dec(res).rotate(-2)
        return sane_hex(d)[:self.max_len]


class PD5(object):
    '''
    A hasher that is much faster than PD4(), but more suited for generating 
    checksums than password storage because of its limited length (23 - 30 
    characters)
    
    AUTHORS:
    v0.3.0+             --> pydsigner
    '''
    max_len = 128
    mag_num = int(dec(40).exp())
    
    def encode(self, s):
        L = self.mag_num * len(s)
        r = int(str(hash(s) * L).replace('-', str(self.max_len)))
        return sane_hex(r)[:self.max_len]


class PD6(object):
    '''
    A hasher that is slower than PD5(), but better suited for password 
    storage and much faster than PD4(). WARNING: It is not recommended that one 
    use this hasher on strings more than 256 characters long.
    
    AUTHORS:
    v0.3.1+             --> pydsigner
    '''
    max_len = 128
    mag_num = int(dec(46).exp())
    split_size = 2
    dash = mag_num // 3
    
    def encode(self,  s):
        z = len(s) // self.split_size
        z += 1 if len(s) % self.split_size else 0
        bitesize = self.max_len * 2 * self.split_size
        sec = iter_utils.section(s[:bitesize], self.split_size)
        L = self.mag_num * z
        r = int(''.join([str(hash(s) * L).replace('-', str(self.dash)
                ) for s in sec]))
        return sane_hex(r)[:self.max_len]


class PD7(PD6):
    '''
    A fast checksum generator similar to, but slower than, the popular md5. 
    For a longer generator, see PD8(). WARNING: It is not recommended that one 
    use this hasher on strings more than 128 characters long.
    
    AUTHORS:
    v0.3.6+             --> pydsigner
    '''
    max_len = 32
    mag_num = 68
    split_size = 4
    dash = mag_num // 5


class PD8(PD6):
    '''
    A checksum generator designed to be right between PD7() and PD6() in 
    terms of speed and quality. WARNING: It is not recommended that one use 
    this hasher on strings more than 192 characters long.
    
    AUTHORS:
    v0.3.4+             --> pydsigner
    '''
    max_len = 64
    mag_num = 57
    split_size = 3
    dash = (mag_num * 6) // 19


class PD9(object):
    '''
    A hasher designed to replace PD6().
    
    AUTHORS:
    v0.3.5+             --> pydsigner
    '''
    max_len = 128
    mag_num = int(dec(53).exp())
    split_size = 2
    dash = str((mag_num * 2) // 7)
    
    def encode(self, s):
        z = len(s) // self.split_size
        z += 1 if len(s) % self.split_size else 0
        bitesize = self.max_len * 2 * self.split_size
        sec = iter_utils.section(s[:bitesize], self.split_size)
        L = self.mag_num * z
        v = ''.join([str(hash(s[bitesize:]))] + 
                    [str(hash(s) * L).replace('-', self.dash) for s in sec])
        r = int(v)
        return sane_hex(r)[:self.max_len]


class PD10(PD9):
    '''
    A hasher designed to replace PD7().
    
    AUTHORS:
    v0.3.5+             --> pydsigner
    '''
    max_len = 32
    mag_num = int(dec(57).exp())
    split_size = 4
    dash = str(mag_num // 4)


class PD11(PD9):
    '''
    A hasher designed to replace PD8().
    
    AUTHORS:
    v0.3.5+             --> pydsigner
    '''
    max_len = 64
    mag_num = int(dec(43).exp()) * 9
    split_size = 3
    dash = str(int(dec(31).exp()))


class PD12(object):
    '''
    Similar to but not the same as PD9().
    
    AUTHORS:
    v0.3.6+             --> pydsigner
    '''
    max_len = 128
    mag_num = 7
    split_size = 2
    dash = str(int(dec(23).exp()))
    
    def encode(self, s):
        z = len(s) // self.split_size
        z += 1 if len(s) % self.split_size else 0
        bitesize = self.max_len * 2 * self.split_size
        sec = iter_utils.section(s[:bitesize], self.split_size)
        end = s[bitesize:]
        end36 = iter_utils.keep_many(end, string.ascii_letters + string.digits)
        q = int(end36, 36) if end36 else 0
        ds = int(self.dash)
        if q < ds * 2 // 3 or not q or q < 0:
            q = ds
        L = self.mag_num * z * q
        v = ''.join([str(hash(end))] + [str(hash(s) * L
                ).replace('-', self.dash) for s in sec])
        r = int(v)
        return sane_hex(r)[:self.max_len]


class PD13(PD12):
    '''
    Similar to PD10() but based on PD12().
    
    AUTHORS:
    v0.3.6+             --> pydsigner
    '''
    max_len = 32
    mag_num = 3
    split_size = 4
    dash = str(int(dec(13).exp()))


class PD14(PD12):
    '''
    Similar to PD11() but based on PD12().
    
    AUTHORS:
    v0.3.6+             --> pydsigner
    '''
    max_len = 64
    mag_num = 5
    split_size = 3
    dash = str(int(dec(17).exp()))


class RD(object):
    '''
    Seeds the random module with the object to be hashed; returns the str()ed 
    result of random.randint(self.small, self.big). Possible weaknesses: Does 
    random return the same numbers on all platforms? Will threading break 
    this?
    
    AUTHORS:
    v0.4.7+             --> pydsigner
    '''
    small = 0
    big = 10 ** 10
    
    def encode(self, s):
        random.seed(s)
        return str(random.randint(self.small, self.big))


class SHA1(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return hashlib.sha1(s).hexdigest()


class SHA224(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return hashlib.sha224(s).hexdigest()


class SHA256(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return hashlib.sha256(s).hexdigest()


class SHA384(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return hashlib.sha384(s).hexdigest()


class SHA512(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return hashlib.sha512(s).hexdigest()


class MD5(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return hashlib.md5(s).hexdigest()


class Base16(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return base64.b16encode(s)
    def decode(self, s):
        return base64.b16decode(s)


class Base32(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return base64.b32encode(s)
    def decode(self, s):
        return base64.b32decode(s)


class Base64(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return base64.b64encode(s)
    def decode(self, s):
        return base64.b64decode(s)


class Hex(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return binascii.b2a_hex(s)
    def decode(self, s):
        return binascii.a2b_hex(s)


class HQX(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return binascii.b2a_hqx(s)
    def decode(self, s):
        return binascii.a2b_hqx(s)[0]


class UU(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return binascii.b2a_uu(s)
    def decode(self, s):
        return binascii.a2b_uu(s)


class URL(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    def encode(self, s):
        return urler.quote(s)
    def decode(self, s):
        return urler.unquote(s)


class HTML(object):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    conv_dict = {'<': '&#60;', '>': '&#62;', '"': '&#34;', '&': '&#38;'}
    
    def encode(self, s):
        return iter_utils.many(s, self.conv_dict)
    def decode(self, s):
        return iter_utils.many(s, self.conv_dict, True)


class CRC32(object):
    '''
    AUTHORS:
    v0.2.7+             --> pydsigner
    '''
    def encode(self, s):
        return zlib.crc32(s)


class Adler32(object):
    '''AUTHORS:
    v0.2.7+             --> pydsigner'''
    def encode(self, s):
        return zlib.adler32(s)


encoder_classes = dict(triplets=Triplets, pd2=PD2, pd3=PD3, pd4=PD4, pd5=PD5, 
                       pd6=PD6, pd7=PD7, pd8=PD8, pd9=PD9, pd10=PD10, 
                       pd11=PD11, pd12=PD12, pd13=PD13, pd14=PD14, rd=RD, 
                       sha1=SHA1, sha224=SHA224, sha256=SHA256, sha384=SHA384, 
                       sha512=SHA512, md5=MD5, base16=Base16, base32=Base32, 
                       base64=Base64, hex=Hex, hqx=HQX, uu=UU, url=URL, 
                       html=HTML, crc32=CRC32, adler32=Adler32)


def fetcher(encoder):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    return encoder_classes[encoder.lower()]()


def rand_key(L=10):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    res = ''
    while len(res) < L:
        v = str(math.log((random.randint(1, 33) * math.pi) ** 2))
        res += iter_utils.remove_many(v, 'e-.')
    return res[:L]


def multi_pass(user, pswd, times=1000, hasher=SHA512()):
    '''
    AUTHORS:
    v0.2.0+             --> pydsigner
    '''
    for i in range(times):
        pswd = hasher.encode(pswd + user + str(i))
    return pswd
