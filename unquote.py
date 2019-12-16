# รวม def โค๊ดนี้เข้าไปในโค๊ดของท่าน

hexdig = '0123456789ABCDEFabcdef'
_hextochr = dict((a + b, chr(int(a + b, 16)))
                 for a in _hexdig for b in _hexdig)

def unquote(ss):
	"""unquote('abc%20def') -> 'abc def'."""
	for i in range(len(ss)):
		if ss[i:i+1] == '+':
			ss = ss[:i]+' '+ss[i+1:]
	res = ss.split('%')
	utf = 0
	hex1 = 0
	hex2 = 0
	# fastpath
	if len(res) == 1:
		return ss
	ss = res[0]
	for item in res[1:]:
		if utf == 2:
			hex2 = _hextochr[item[:2]]
			if (ord(hex1)*256)+ord(hex2) >= 47488:
				ss += chr((ord(hex1)*256)+ord(hex2)-43840) + item[2:]			
			else:
				ss += chr((ord(hex1)*256)+ord(hex2)-43648) + item[2:]
			utf = 0
			continue
		if utf == 1:
			hex1 = _hextochr[item[:2]]
			utf = 2
			continue
		if item[:2] == 'E0' or item[:2] == 'e0':
			utf = 1
			continue
		try:
			ss += _hextochr[item[:2]] + item[2:]
		except KeyError:
			ss += '%' + item
		except:
			ss += chr(int(item[:2], 16)) + item[2:]
	return ss
