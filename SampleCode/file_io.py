import machine
import uos as os

#disable USB mass storage
machine.msc_disable()

filelist = os.listdir()
new_file = open ('test.txt','w')
new_file.write('some data')
new_file.close()

f = open ('test.txt',r')
print (f.read())

bin_file = open('test.bin','w+b')
bin_file.write(b'\x01\xff\x90\x04\xae')
bin_file.write(b'abcde')
bin_file.close ()

bin_file = open('test.bin','r+b')
print (bin_file.read())
bin_file.close ()


bin_file = open('test.bin','a+b') #append
bin_file.write(b'1234555')
bin_file.close ()

machine.msc_enable()

