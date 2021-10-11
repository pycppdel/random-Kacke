#include <SDL.h>
#include <iostream>

struct Display{

SDL_Window* window;
SDL_Surface* screen;

};

struct Display* Init();

void end(SDL_Window* win);


int main(){

  struct Display* dis = Init();
  SDL_FillRect(dis->screen, NULL, SDL_MapRGB(dis->screen->format, 0x44, 0xC9, 0x77));
  SDL_UpdateWindowSurface(dis->window);
  SDL_Delay(2000);
  end(dis->window);


}

struct Display* Init(){

Display* dis = new Display;
dis->window = NULL;
dis->screen = NULL;

SDL_Init(SDL_INIT_VIDEO);

dis->window = SDL_CreateWindow("TT", 200, 200, 800, 800, SDL_WINDOW_SHOWN);
dis->screen = SDL_GetWindowSurface(dis->window);

return dis;

}
void end(SDL_Window* win){

SDL_DestroyWindow(win);
SDL_Quit();

}
