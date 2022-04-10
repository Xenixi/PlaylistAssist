#include <stdlib.h>
#include <stdio.h>
int main() {
    printf("Launching in background... ctrl+shift+f1 exits. You may close this window, process will remain active.");
    system("pythonw PlAs.py");
    return 0;
};