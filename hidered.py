from PIL import Image
from pathlib import Path
import binascii
import optparse
import cv2
import numpy as np

def rgb2hex(r,g,b):
	return '#{:02x}{:02x}{:02x}'.format(r,g,b)
	
def hex2rgb(hexcode):
	return tuple(map(ord,hexcode[1:].decode('hex')))
	
	
def str2bin(message):
	binary=bin(int(binascii.hexlify(message),16))
	return binary[2:]


def bin2str(binary):
	message=binascii.unhexlify('%x' % (int('0b'  +binary,2)))
	return message
	
	
def encode(hexcode,digit,item):
	if hexcode[2] in('0','1','2','3','4','5','6','7','8','9'):
		print item," Hexcode before:",hexcode, " Equivalent RGB before:",hex2rgb(hexcode)
		print "Hexcode[:2]: ",hexcode[:2]," Digit value: ",digit," Hexcode[3:]",hexcode[3:]
		hexcode=hexcode[:2]+digit+hexcode[3:]
		print item," Hexcode after:",hexcode, " Equivalent RGB after:",hex2rgb(hexcode),"\n"
		return hexcode
	else:
		return None


def decode(hexcode):
	if hexcode[2] in('0','1'):
		return hexcode[2]
	else:
		return None



def hide(filename,message):
	img=Image.open(filename)
	print 'Message:',message
	binary=str2bin(message)+ '1111111111111110'
	print 'Binary:',binary
	if img.mode in ('RGBA'):
		img2=img.convert('RGBA')
		datas=img2.getdata()
		
		newData=[]
		digit=0
		temp=''
		for item in datas:
			if(digit<len(binary)):
				#Every pixel changed in the image  
				#print 'Red int:',item[0],' Green int:',item[1],' Blue int:',item[2],' RGB hex:',rgb2hex(item[0],item[1],item[2])

				newpix=encode(rgb2hex(item[0],item[1],item[2]),binary[digit],digit)
				if newpix==None:
					newData.append(item)
				else:
					r,g,b=hex2rgb(newpix)
					newData.append((r,g,b,255))
					digit=digit+1
			else:
				newData.append(item)
		img2.putdata(newData)
		img2.save(filename+"red","png")
		return "Completed"
	return "Incorrect Image mode,could not hide"


def retr(filename):
	img=Image.open(filename)
	binary=''
	
	if img.mode in('RGBA'):
		img=img.convert('RGBA')
		datas=img.getdata()
		
		for item in datas:
			digit=decode(rgb2hex(item[0],item[1],item[2]))
			
			if digit==None:
				pass
			else:
				binary=binary+digit
				if(binary[-16:]=='1111111111111110'):
					print "Success"
					return bin2str(binary[:-16])
		return bin2str(binary)
	return "Incorrect Image mode,could not retrieved"

def difference(filename):
	image1 = cv2.imread(filename)
	stego_image = Path("/home/abhireus/Documents/Image Processing/4/"+filename+"red")
	if stego_image.is_file():
		image2 = cv2.imread(filename+"red")
	else:
		image2 = cv2.imread(filename)

	difference = cv2.subtract(image1, image2)
	result = not np.any(difference)

	if result is True:
		print "The images are same"
	else:
		cv2.imwrite("redresult.png", difference)
		print "the images are different"

def Main():
	parser=optparse.OptionParser('usage%prog'+\
	       '-e/-d<target file>')
	parser.add_option('-e',dest='hide',type='string', \
	help='target picture path to hide text')
	parser.add_option('-d',dest='retr',type='string', \
	help='target picture path to retrieve text')
	
	(options,args)=parser.parse_args()
	if(options.hide!=None):
		text=raw_input("enter a message to hide:")
		difference(options.hide)
		print hide(options.hide,text)
	elif(options.retr!=None):
		print retr(options.retr)
	else:
		print parser.usage
		exit(0)

if __name__=='__main__':
	Main()

			
