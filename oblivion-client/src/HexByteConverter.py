#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""Hex String <-> Byte Array Converter

16진수 문자열과 Byte 배열을 전환해주는 라이브러리입니다.

ByteToHex converts byte string "\xFF\xFE\x00\x01" to the string "FF FE 00 01"
HexToByte converts string "FF FE 00 01" to the byte string "\xFF\xFE\x00\x01"
"""

def ByteToHex( byteStr ):
	"""
	Convert a byte string to it's hex string representation e.g. for output.
	"""

	return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

def HexToByte( hexStr ):
	"""
	Convert a string hex byte values into a byte string. The Hex Byte values may
	or may not be space separated.
	"""

	bytes = []

	hexStr = ''.join( hexStr.split(" ") )

	for i in range(0, len(hexStr), 2):
		bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

	return ''.join( bytes )


# test data - different formats but equivalent data
__hexStr1  = "FFFFFF5F8121070C0000FFFFFFFF5F8129010B"
__hexStr2  = "FF FF FF 5F 81 21 07 0C 00 00 FF FF FF FF 5F 81 29 01 0B"
__byteStr = "\xFF\xFF\xFF\x5F\x81\x21\x07\x0C\x00\x00\xFF\xFF\xFF\xFF\x5F\x81\x29\x01\x0B"


if __name__ == "__main__":
	print "\nHex To Byte and Byte To Hex Conversion"

	print "Test 1 - ByteToHex - Passed: ", ByteToHex( __byteStr ) == __hexStr2
	print "Test 2 - HexToByte - Passed: ", HexToByte( __hexStr1 ) == __byteStr
	print "Test 3 - HexToByte - Passed: ", HexToByte( __hexStr2 ) == __byteStr

	# turn a non-space separated hex string into a space separated hex string!
	print "Test 4 - Combined  - Passed: ", \
		ByteToHex( HexToByte( __hexStr1 ) ) == __hexStr2

	if __name__ == "__main__":
		print "Hex String <-> Byte Array Converter"