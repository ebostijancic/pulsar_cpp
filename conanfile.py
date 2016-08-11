from conans import ConanFile, CMake, tools
import os


class PulsarConan(ConanFile):
    name = "Pulsar"
    version = "0.0.1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
       self.run("git clone https://github.com/ebostijancic/pulsar_cpp")
       # self.run("cd hello && git checkout static_shared")
       # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
       # if the packaged project doesn't have variables to set it properly
       tools.replace_in_file("pulsar_cpp/CMakeLists.txt", "PROJECT(pulsar_cpp)", '''PROJECT(pulsar_cpp)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake pulsar_cpp %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.hpp", dst="include", src="include/pulsar")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]
