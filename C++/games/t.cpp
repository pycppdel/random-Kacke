#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <iostream>


struct Display{

SDL_Window* window;
SDL_Surface* screen;

};

SDL_Surface** images;
int show=0;

struct Display* start(int, int);
SDL_Surface* load();
void end(struct Display*);

int main(){

  images = new SDL_Surface*[10];


  SDL_Init(SDL_INIT_VIDEO);
  IMG_Init(IMG_INIT_PNG);

  images[0] = load();

  struct Display* d = start(800, 800);

  //SDL_FillRect(d->screen, NULL, SDL_MapRGB(d->screen->format, 0x44, 0x87, 0x88));
  SDL_Rect rect;
  rect.x = 0;
  rect.y = 0;
  rect.w = 1920;
  rect.h = 1080;
  for(int z = 0; z < 100; z++){
    SDL_FillRect(d->screen, NULL, SDL_MapRGB(d->screen->format, 0, 0, 0));
    rect.x -= 10;
    SDL_BlitSurface(images[0], &rect, d->screen, NULL);
    SDL_UpdateWindowSurface(d->window);

    SDL_Delay(100);
  }

  end(d);

  delete [] images;


  return 0;
}

struct Display* start(int width, int height){

  struct Display* back;
  back = new Display;

  back->window = SDL_CreateWindow("__", 100, 100, width, height, SDL_WINDOW_SHOWN);
  //SDL_SetWindowFullscreen(back->window, SDL_WINDOW_FULLSCREEN_DESKTOP);
  back->screen = SDL_GetWindowSurface(back->window);

  return back;

}

SDL_Surface* load(){

  return IMG_Load("back.png");

}

void end(struct Display* dis){

  SDL_DestroyWindow(dis->window);

  for(int i=0;i<10;i++){
    SDL_FreeSurface(::images[i]);
  }

  SDL_Quit();
}
