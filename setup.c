/*
 * ******************************************************
 * Playlist Assist Setup / Kobe McManus (Xenixi), 2022 *
 * ******************************************************
 */
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <stdbool.h>
#include <string.h>

// **********************************************************************************

static const char *python_latest = "3.10.4";
static const int acceptable_versions_quantity = 4;
static const char *python_acceptable_versions[] =
    {"3.10.", "3.9.", "3.8.", "3.7."};

// **********************************************************************************
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
            break;
        }
        else
        {
            for (int i = 0; i < (acceptable_versions_quantity - 1); i++)
            {
                if (strstr(read, python_acceptable_versions[i]) != NULL)
                {
                    match = true;
                    break;
                }
            }
        }
    }

    printf("Adequate Python Version installed: ");
    printf(match ? "true\n" : "false\n");

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
    else
    {
        printf("Skipping Python installation step...\n");
    }

    printf("Installing Python packages...\n");

    fp = popen("pip install spotipy && pip install pynput && pip install chime", "r");

    char read2[1024];

    while (fgets(read2, sizeof(read2), fp))
    {
        printf("%s", read2);
    }

    // Sleep(1500);

    printf("\nInstalling shortcuts...\n");

    printf("\n**Skipping this step...\n");

    printf("\nClearing cache...");
    for (int i = 0; i < 10; i++)
    {
        if (remove(".cache") == 0)
        {
            printf("\nCache cleared.\n");
            break;
        }
        else
        {
            Sleep(500);
            if (i == 9)
            {
                printf("\nCache not cleared: either busy or doesn't exist.");
            }
        }
    }

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