CFLAGS += -std=c99

all: test_np test_fs

test_fs: test_fs.o lo_pass.o

test: lo_pass test.py
	python2 test.py

test_np: wrapper.c lo_pass.c
	-rm -r build/
	python2 setup.py build

clean:
	-rm test_fs
	-rm *.o *~
	-rm -r build/
	-rm input.bin output.bin test1.png test2.png
