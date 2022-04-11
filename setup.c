#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <stdbool.h>
#include <string.h>
static const char *python_latest = "3.10.4";

int main(void)
{
    FILE *fp;

    printf("Running setup...\nChecking Python version...\n");
    //  Sleep(500);
    fp = popen("python --version", "r");

    char read[64];

    bool match = false;
    while (fgets(read, sizeof(read), fp))
    {
        printf("%s", read);
        if (strstr(read, python_latest) != NULL)
        {
            match = true;
        }
    }

    printf("Matching version: ");
    printf(match ? "true" : "false");

    if (!match)
    {

        char read[1024];

        fp = popen("curl https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe --output pyinstaller.exe && pyinstaller.exe InstallAllUsers=1 PrependPath=1", "r");

        while (fgets(read, sizeof(read), fp))
        {
            printf("%s", read);
        }

        printf("Finished running new installer for Python\n");

        while (true)
        {
            if (remove("pyinstaller.exe") == 0)
            {
                break;
            }
        }

        // Sleep(1500);
    }

    printf("Installing python packages...\n");

    fp = popen("pip install spotipy && pip install keyboard && pip install chime", "r");

    char read2[1024];

    while (fgets(read2, sizeof(read2), fp))
    {
        printf("%s", read2);
    }

    // Sleep(1500);

    printf("\nInstalling shortcuts...\n");

    printf("\n**Skipping this step...\n");

    // Sleep(500);

    // fp = popen("powershell -Command \"Start-Process python setup2.py -Verb RunAs\"", "r");

    while (fgets(read2, sizeof(read2), fp))
    {
        printf("%s", read2);
    }

    printf("\nOperation completed.\n");

    // pause
    printf("Press any key to exit.");
    getchar();

    pclose(fp);

    return (0);
};