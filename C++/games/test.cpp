#include <SDL.h>
#include <iostream>


struct Display{

SDL_Window* window;
SDL_Surface* screen;

};

struct Display* start(int, int);
void end(struct Display*);

int main(){


  return 0;
}

struct Display* start(int width, int height){

  struct Display* back;
  back = new Display(NULL, NULL);

  back->window = SDL_CreateWindow("__", 100, 100, width, height);
  back->screen = SDL_GetWindowSurface(back->window);

  return back;

}

void end(struct Display* dis){

  SDL_Destroy(dis->window);
  SDL_Quit();
}
