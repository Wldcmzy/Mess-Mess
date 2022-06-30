#include <cstdio>
#include <iostream>
//#include <conio.h>
#include <windows.h>
#include <time.h>

#define POS_START ((POINT){1090, 681})
#define POS_SELF ((POINT){768, 647})
#define POS_SKILL ((POINT){894, 632})
#define POS_END_TURN ((POINT){1200, 390})
#define POS_STAET_GAME ((POINT){621, 594})
#define POS_SAY1 ((POINT){660, 534})
#define POS_SAY2 ((POINT){621, 594})
#define POS_SAY3 ((POINT){618, 661})
#define POS_SAY4 ((POINT){874, 531})
#define POS_SAY5 ((POINT){910, 598})
#define POS_SAY6 ((POINT){906, 667})
#define DELAY_START 5
#define DELAY_SKILL 13
#define DELAY_SAY 31
#define DELAY_END_TURN 127

POINT talks[7] = {
    POS_SAY1, 
    POS_SAY1, 
    POS_SAY2, 
    POS_SAY3, 
    POS_SAY4, 
    POS_SAY5, 
    POS_SAY6
};
const int talk_rand_list_size = 22;
int talk_rand_list[talk_rand_list_size] = {
    1, 1,
    2, 2, 2, 
    3, 3, 3, 3,
    4, 4, 4, 4, 4, 4,
    5, 5, 5,
    6, 6, 6, 6 ,   
};

void Cursor_Pos_Loop(){
    POINT point;
    GetCursorPos(&point);
    printf("%-10d%-10d\n", point.x, point.y);
}

void Left_Click(POINT point){
    SetCursorPos(point.x, point.y);
    mouse_event(MOUSEEVENTF_LEFTDOWN,0,0,0,0);
    Sleep(25);
    mouse_event(MOUSEEVENTF_LEFTUP,0,0,0,0);
}
void Right_Click(POINT point){
    SetCursorPos(point.x, point.y);
    mouse_event(MOUSEEVENTF_RIGHTDOWN,0,0,0,0);
    Sleep(25);
    mouse_event(MOUSEEVENTF_RIGHTUP,0,0,0,0);
}

int counter_end_turn = 0;
int counter_start = 0;
int counter_skill = 0;
int counter_say[7] = {0};
void show(){
    printf("ENDTURN:%d\n", counter_end_turn);
    printf("START:%d\n", counter_start);
    printf("SKILL:%d\n", counter_skill);
    printf("3Q:%d\n", counter_say[1]);
    printf("Unb:%d\n", counter_say[2]);
    printf("hi:%d\n", counter_say[3]);
    printf("WoW:%d\n", counter_say[4]);
    printf("no:%d\n", counter_say[5]);
    printf("cnm:%d\n", counter_say[6]);
}

void run(){
    time_t startTime = time(NULL), timmer;
    printf("start after 5s...\n");
    Sleep(5000);
    printf("start!\n");
    while(true){
        timmer = time(NULL) - startTime;
        if(timmer % 60 == 0){
            printf("%dhours %dmin\n", timmer / 3600, (timmer % 3600) / 60);
        }
        
        if(!(timmer % DELAY_END_TURN)){
            Left_Click(POS_END_TURN);
            counter_end_turn += 1;
        }else if(!(timmer % DELAY_SAY)){
            Right_Click(POS_SELF);
            Sleep(500);
            int pos = talk_rand_list[(rand() % talk_rand_list_size) + 1];
            Left_Click(talks[pos]);
            counter_say[pos] += 1;
            show();
        }else if(!(timmer % DELAY_SKILL)){
            Left_Click(POS_SKILL);
            Sleep(500);
            Left_Click(POS_SELF);
            counter_skill += 1;
        }else if(!(timmer % DELAY_START)){
            Left_Click(POS_START);
            counter_start += 1;
        }
        Sleep(800);
    }
}

void findPos(int delay = 250){
    while(true){
        Cursor_Pos_Loop();
        Sleep(delay);
    }
}

int main(){
    //findPos();
    run();
    return 0;
}
