import machine
import _thread
import utime
def testThread1():
	while True:
		print("Hello from thread_1")
		utime.sleep(2)
 
 
def testThread2():
	while True:
		print("Hello from thread_2")
		utime.sleep(1)
 
_thread.start_new_thread(testThread1, ())
_thread.start_new_thread(testThread2, ())
