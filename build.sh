echo "Building to 'Build/'"
rm -r Build/
mkdir Build/
gcc setup.c -o Build/setup.exe
gcc launch.c -o Build/launch.exe
gcc launch-background.c -o Build/launch-background.exe
cp PlAs.py Build/PlAs.py
cp README.md Build/README.md
echo "Build Completed."
