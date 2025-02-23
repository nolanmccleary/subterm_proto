default: cffi

cffi: _whisper_cpp.*.so

_whisper_cpp.*.so: whisper_cpp/build/src/libwhisper.so
	python3 whisper_cffi_build.py

#whisper_cpp/CMakeLists.txt:
#	git submodule update --init --recursive

whisper.cpp/build/src/libwhisper.so: whisper_cpp/CMakeLists.txt
	cd whisper_cpp && cmake -B build && cmake --build build --config Release

clean:
	rm -rf _whisper_cpp.* libwhisper.so* whisper_cpp/build/