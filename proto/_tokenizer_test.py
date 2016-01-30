
import unittest
from proto._tokenizer import _Tokenizer, _WireTypes
import cStringIO

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = _Tokenizer()
        
    def testWriteVarIntZero(self):
        output = cStringIO.StringIO()
        self.tokenizer.write_varint(output, 0)
        
        self.assertEquals(output.getvalue().encode('hex'), '00')
    
    def testWriteVarIntOne(self):
        output = cStringIO.StringIO()
        self.tokenizer.write_varint(output, 1)
        
        self.assertEquals(output.getvalue().encode('hex'), '01')
    
    def testWriteVarIntAllBitsExceptLastSet(self):
        output = cStringIO.StringIO()
        self.tokenizer.write_varint(output, 127)
        
        self.assertEquals(output.getvalue().encode('hex'), '7f')
        
    def testWriteVarIntTwoBytesFirstBitOfSecondByteSet(self):
        output = cStringIO.StringIO()
        self.tokenizer.write_varint(output, 128)
        
        self.assertEquals(output.getvalue().encode('hex'), '8001')
        
    def testWriteVarIntTwoBytes300(self):
        output = cStringIO.StringIO()
        self.tokenizer.write_varint(output, 300)
        
        self.assertEquals(output.getvalue().encode('hex'), 'ac02')
        
    
    
    def testReadVarInt(self):
        input = cStringIO.StringIO('01'.decode('hex'))
        num = self.tokenizer.read_varint(input)
        
        self.assertEquals(1, num)
        
        
    def testWriteKeyVarInt(self):
        output = cStringIO.StringIO()
        self.tokenizer.write_key(output, _WireTypes.VAR_INT, 2)
        
        self.assertEquals(output.getvalue().encode('hex'), '04')
        
    def testWriteKeyLengthDelimited(self):
        output = cStringIO.StringIO()
        self.tokenizer.write_key(output, _WireTypes.LENGTH_DELIMITED, 2)
        
        self.assertEquals(output.getvalue().encode('hex'), '05')
        
        
    def testReadKeyVarInt(self):
        input = cStringIO.StringIO('04'.decode('hex'))
        key = self.tokenizer.read_key(input)
        
        self.assertEqual(key, (2, _WireTypes.VAR_INT))
        
    def testReadKeyLengthDelimited(self):
        input = cStringIO.StringIO('05'.decode('hex'))
        key = self.tokenizer.read_key(input)
        
        self.assertEqual(key, (2, _WireTypes.LENGTH_DELIMITED))
    
if __name__ == '__main__':
    unittest.main()