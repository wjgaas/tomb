all:runnable_so.exe \
	test_spirit.exe \
	test_bind.exe \
	test_proto_dynamic.exe

runnable_so.exe:runnable_so.o
	g++ -o $@ $^ -shared -e so_main
%.exe:%.o
	g++ -o $@ $^

%.o:%.cc
	g++ -o $@ $^ -fPIC -c -g

clean:
	rm -rf *.exe *.o

test_proto_dynamic.exe:test_proto_dynamic.o sample.pb.o
	g++ -o $@ $^ -lprotobuf
sample.pb.cc sample.pb.h:sample.proto
	protoc --cpp_out=. $^
