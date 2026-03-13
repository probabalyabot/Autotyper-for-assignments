/*
 * MATRIX RAIN — Windows Console Animation in C
 * Showcases: Win32 Console API, structs, signal handling, heap allocation
 *
 * Compile: gcc code.c -o code
 * Run:     .\code
 * Quit:    Ctrl+C  or  Q  or  ESC
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <signal.h>
#include <windows.h>
#include <conio.h>

/* ── Config ─────────────────────────────────────────────────────────── */
#define MAX_COLS      512
#define FRAME_DELAY   40
#define MIN_SPEED     3
#define MAX_SPEED     12
#define TRAIL_LEN     20

static const char GLYPHS[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    "@#$%&*<>[]{}|/\\~^`:.,-=+?!";
#define GLYPH_COUNT (int)(sizeof(GLYPHS) - 1)

#define COLOR_BLACK    0
#define COLOR_DK_GREEN FOREGROUND_GREEN
#define COLOR_BR_GREEN (FOREGROUND_GREEN | FOREGROUND_INTENSITY)
#define COLOR_WHITE    (FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)

/* ── Column state ───────────────────────────────────────────────────── */
typedef struct {
    int  head;
    int  speed;
    int  tick;
    int  length;
    char glyphs[256];
    int  active;
    int  pause;
} Column;

/* ── Globals ────────────────────────────────────────────────────────── */
static volatile int g_running = 1;
static HANDLE       g_hOut;
static int          g_rows, g_cols;

/* ── Helpers ────────────────────────────────────────────────────────── */
static char rand_glyph(void) { return GLYPHS[rand() % GLYPH_COUNT]; }

static void move_and_draw(int row, int col, char ch, WORD color) {
    COORD pos = { (SHORT)col, (SHORT)row };
    DWORD written;
    SetConsoleTextAttribute(g_hOut, color);
    SetConsoleCursorPosition(g_hOut, pos);
    WriteConsoleA(g_hOut, &ch, 1, &written, NULL);
}

static void get_console_size(int *rows, int *cols) {
    CONSOLE_SCREEN_BUFFER_INFO info;
    GetConsoleScreenBufferInfo(g_hOut, &info);
    *cols = info.srWindow.Right  - info.srWindow.Left + 1;
    *rows = info.srWindow.Bottom - info.srWindow.Top  + 1;
}

static void hide_cursor(void) {
    CONSOLE_CURSOR_INFO ci = { 1, FALSE };
    SetConsoleCursorInfo(g_hOut, &ci);
}

static void show_cursor(void) {
    CONSOLE_CURSOR_INFO ci = { 1, TRUE };
    SetConsoleCursorInfo(g_hOut, &ci);
}

static void handle_sigint(int sig) { (void)sig; g_running = 0; }

/* ── Column logic ───────────────────────────────────────────────────── */
static void init_column(Column *c, int rows) {
    c->head   = -(rand() % rows);
    c->speed  = MIN_SPEED + rand() % (MAX_SPEED - MIN_SPEED + 1);
    c->tick   = c->speed;
    c->length = 6 + rand() % (TRAIL_LEN - 6);
    c->active = 1;
    c->pause  = 0;
    for (int i = 0; i < 256; i++)
        c->glyphs[i] = rand_glyph();
}

static void render_column(const Column *c, int col, int rows) {
    int head = c->head;

    for (int offset = 0; offset <= c->length; offset++) {
        int row = head - offset;
        if (row < 0 || row >= rows) continue;

        char ch = c->glyphs[row % 256];
        WORD color = (offset == 0)   ? COLOR_WHITE    :
                     (offset < 3)    ? COLOR_BR_GREEN  :
                                       COLOR_DK_GREEN;
        move_and_draw(row, col, ch, color);
    }

    int erase_row = head - c->length - 1;
    if (erase_row >= 0 && erase_row < rows)
        move_and_draw(erase_row, col, ' ', COLOR_BLACK);
}

/* ── Main ───────────────────────────────────────────────────────────── */
int main(void) {
    srand((unsigned)time(NULL));
    signal(SIGINT, handle_sigint);

    g_hOut = GetStdHandle(STD_OUTPUT_HANDLE);

    system("mode con: cols=120 lines=40");
    SetConsoleTitle("Matrix Rain");
    SetConsoleTextAttribute(g_hOut, COLOR_DK_GREEN);
    system("cls");
    hide_cursor();

    get_console_size(&g_rows, &g_cols);
    int ncols = g_cols < MAX_COLS ? g_cols : MAX_COLS;

    Column *columns = calloc((size_t)ncols, sizeof(Column));
    if (!columns) { fprintf(stderr, "calloc failed\n"); return 1; }

    for (int c = 0; c < ncols; c++) {
        init_column(&columns[c], g_rows);
        columns[c].head -= rand() % g_rows;
    }

    while (g_running) {
        if (_kbhit()) {
            int k = _getch();
            if (k == 27 || k == 'q' || k == 'Q') break;
        }

        for (int c = 0; c < ncols; c++) {
            Column *col = &columns[c];

            if (!col->active) {
                if (--col->pause <= 0) init_column(col, g_rows);
                continue;
            }

            col->glyphs[rand() % 256] = rand_glyph();

            if (--col->tick <= 0) {
                col->tick = col->speed;
                col->head++;
            }

            render_column(col, c, g_rows);

            if (col->head - col->length > g_rows) {
                col->active = 0;
                col->pause  = rand() % (g_rows / 2);
            }
        }

        Sleep(FRAME_DELAY);
    }

    show_cursor();
    SetConsoleTextAttribute(g_hOut, COLOR_WHITE);
    system("cls");
    free(columns);
    return 0;
}