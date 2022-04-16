echo "Building to 'Build/'"
rm -r Build/
mkdir Build/
windres plas.rc plas.o
windres plas_ins.rc plas_ins.o
windres plas_background.rc plas_background.o
gcc setup.c plas_ins.o -o Build/setup.exe
gcc launch.c plas.o -o Build/launch.exe
gcc launch-background.c plas_background.o -o Build/launch-background.exe
rm plas_ins.o
rm plas.o
rm plas_background.o
cp PlAs.py Build/PlAs.py
cp README.md Build/README.md
echo "Build Completed."
