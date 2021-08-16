from PIL import Image
import argparse
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
	print("The Encoded message is saved in",f"{a[0]}en.png")
	


def Decode(Dec_Img):
	print("Decoding Message...")
	_img = Image.open(Dec_Img)
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
	parser = argparse.ArgumentParser('python morsesteg.py')
	parser.add_argument('-e',dest='Enc_Img',type=str,help='To Encode a message into an image')
	parser.add_argument('-d',dest='Dec_Img',type=str,help='To Decode a message from an image')
	options = parser.parse_args()
	if (options.Enc_Img == None and options.Dec_Img == None):
		print (parser.usage)
		exit(0)
	elif(options.Dec_Img != None):
		Dec_Img = options.Dec_Img
		Decode(Dec_Img)
	else:
		Enc_Img = options.Enc_Img
		datatoencode = input("Enter the data to Encode :")
		Encoding(datatoencode.upper(),Enc_Img)
		
if __name__ == '__main__':
	Main()