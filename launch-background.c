/*
 * ***********************************************
 * Playlist Assist / Kobe McManus (Xenixi), 2022 *
 * ***********************************************
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int main(int argc, char *argv[])
{
    if (argc == 2 && strcmp(argv[1], "-s") == 0)
    {
        system("start pythonw PlAs.py");
        return 0;
    }
    else
    {
        printf("Launching in background... ctrl+shift+f1 exits. You may close this window, process will remain active.");
        system("pythonw PlAs.py");
        return 0;
    }
};