from PIL import Image
import optparse
import sys
import os


morse_dict={
    #Alphabets
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.',
	'G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..',
	'M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.',
	'S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-',
	'Y':'-.--','Z':'--..',

	#Numbers
	'0':'-----','1':'.----','2':'..---','3':'...--',
	'4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',

	#Special Characters
	'.':'.-.-.-',',':'--..--','?':'..--..',"'":'.----.','/':'-..-.','(':'-.--.-',')':'-.--.-',':':'---...',';':'-.-.-.','=':'-...-','+':'.-.-.','-':'-....-','_':'..--.-','"':'.-..-.','$':'...-..-',' ':'...---...','!':'-.-.--'
	}

reversed_morse_dict = {v: k for k,v in  morse_dict.items()}

def Encoding(inputdata,_PNG):
	assert os.path.exists(_PNG), "File not found, "+str(_PNG)
	letters = list(inputdata)
	pixsum = 0
	Pixels = []
	for letter in letters:
		_morseletter = morse_dict[letter]
		_morsechars = list(_morseletter)
		for morsechar in _morsechars:
			intval = ord(morsechar)
			pixsum += intval
			Pixels.append(pixsum)
		pixsum += 32
		Pixels.append(pixsum)
	img =Image.open(_PNG)
	pixels = img.load()

	for Pixel in Pixels: 
		y= Pixel/100
		x = Pixel%100
		pixels[x,y] = (255,255,255)
	path=_PNG
	a=path.split(".")
	img.save(f"{a[0]}en.png")


def Decode(inPNG):
	_img = Image.open(inPNG)
	W = _img.size[0]   
	H = _img.size[1]
	_pixs = _img.load()
	_prevpix = 0
	_letter = ""
	answer = ""

	for y in range(H):
		for x in range(W):
			if(_pixs[x,y] == (255,255,255)):
				img_pix = y*100 + x - _prevpix
				_prevpix = y*100 + x
				_char = chr(img_pix)
				if(_char != ' '):
					_letter += _char 
				else:
					answer += reversed_morse_dict[_letter]
					_letter = ""
	print (answer)

def Main():
	parser = optparse.OptionParser('usage: python ImageEncoder.py -e or -d <output PNG image name>')
	parser.add_option('-e',dest='outPNG',type='string',help='Please specify the output image file')
	parser.add_option('-d',dest='inPNG',type='string',help='Please specify the input image file')
	(options,arg) = parser.parse_args()
	if (options.outPNG == None and options.inPNG == None):
		print (parser.usage)
		exit(0)
	elif(options.inPNG != None):
		inPNG = options.inPNG
		Decode(inPNG)
	else:
		outPNG = options.outPNG
		print("The Encoded mesage is stored in a filename endswith (original_filename+en).png  ")
		datatoencode = input("Please enter data to encode :")
		Encoding(datatoencode.upper(),outPNG)
		
if __name__ == '__main__':
	Main()