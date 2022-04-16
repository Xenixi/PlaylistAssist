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
int main(int argc, char *argv[])
{
    char *cmd_begin = "powershell -Command \"Start-Process '";
    char *cmd_end = "' run-installer -Verb RunAs\"";
    char elevate_cmd[4096];
    elevate_cmd[0] = '\0';

    strcat(elevate_cmd, cmd_begin);
    strcat(elevate_cmd, argv[0]);
    strcat(elevate_cmd, cmd_end);

    char *skip_py_cmd_end = "' skip-py-install -Verb RunAs\"";
    char skip_py_cmd[4096];
    skip_py_cmd[0] = '\0';

    strcat(skip_py_cmd, cmd_begin);
    strcat(skip_py_cmd, argv[0]);
    strcat(skip_py_cmd, skip_py_cmd_end);

    if (!(argc == 2 && (strcmp(argv[1], "run-installer") == 0 || strcmp(argv[1], "skip-py-install") == 0)))
    {
        system(elevate_cmd);
        return (1);
    }
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

    if (!match && !(strcmp(argv[1], "skip-py-install") == 0))
    {

        char read[1024];

        char *cmd_begin = "curl https://www.python.org/ftp/python/";
        char *cmd_mid = "/python-";
        char *cmd_end = "-amd64.exe --output pyinstaller.exe && pyinstaller.exe InstallAllUsers=1 PrependPath=1";

        char cmd[1024];
        cmd[0] = '\0';

        strcat(cmd, cmd_begin);
        strcat(cmd, python_latest);
        strcat(cmd, cmd_mid);
        strcat(cmd, python_latest);
        strcat(cmd, cmd_end);

        fp = popen(cmd, "r");

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

        // restart

        system(skip_py_cmd);
        return (0);
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
            Sleep(250);
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

    char usr_choice;
    // NOT YET IMPLEMENTED: START MENU SHORTCUTS
    /*
     printf("\n----\nCreate Start Menu Shortcut?(y/n):");
     usr_choice = getchar();
     getchar();

     if (usr_choice == 'y' && false)
     {
         // install shortcut
         char cmd[4096] = "";
         char *begin_cmd = "mklink /d \"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Playlist Assist\" ";
         char launch_path[2048];
         _fullpath(launch_path, "/", 2048);

         strcat(cmd, begin_cmd);
         strcat(cmd, launch_path);

         fp = popen(cmd, "r");

         char read3[1024];

         while (fgets(read3, sizeof(read3), fp))
         {
             printf("%s", read3);
         }
     }
 */
    printf("\n----\nRun On Startup?(y/n):");

    usr_choice = getchar();

    if (usr_choice == 'y')
    {
        // install startup shortcut
        char cmd[4096] = "echo cd /d \"";
        char launch_path[2048];

        _fullpath(launch_path, "launch-background.exe", 2048);

        char *end_cmd = " -s >> \"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/StartupPlaylistAssist.bat\"";

        strcat(cmd, launch_path);
        strcat(cmd, "/..\" ^&^& ");
        strcat(cmd, launch_path);
        strcat(cmd, end_cmd);

        for (int i = 0; i < 10; i++)
        {
            if (remove("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/StartupPlaylistAssist.bat") == 0)
            {
                printf("\nOLD STARTUP FILE REMOVED.");
                break;
            }
            else
            {
                Sleep(250);
                if (i == 9)
                {
                    printf("No pre-existing startup file.");
                }
            }
        }
        fp = popen(cmd, "r");

        char read4[1024];

        while (fgets(read4, sizeof(read4), fp))
        {
            printf("%s", read4);
        }
        printf("\nNEW STARTUP FILE INSTALLED.\n");
    }

    printf("\nOperation completed.\nRUNNING CONSOLE MODE FOR INITIAL SETUP!\n");
    system("start launch.exe");
    // pause
    printf("Press any key to exit this installer.");
    getchar();
    getchar();

    pclose(fp);

    return (0);
};