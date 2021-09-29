#include <SDL.h>
#include <SDL_image.h>
#include <iostream>
#include <ctime>


struct Display{

SDL_Window* window;
SDL_Surface* screen;

};

struct Display* init();
void end(struct Display* d, SDL_Surface* img);

int main(){

  srand(time(NULL));
  struct Display* d = init();
  SDL_Event e;
  bool quit=false;
  SDL_Surface* image;
  image = IMG_Load("back.png");
  image = SDL_ConvertSurface(image, d->screen->format, 0);
  SDL_Rect rect;
  rect.x = -100;rect.y = 0;rect.w = 1980;rect.h=1200;
  while(!quit){

    SDL_PollEvent(&e);

    if (e.type == SDL_QUIT){
      quit = true;

    }

    else if(e.type == SDL_KEYDOWN) {

      if (e.key.keysym.sym == SDLK_i){
        quit = true;
      }

      switch(e.key.keysym.sym){

        case SDLK_UP: rect.y += 10;
                      break;
        case SDLK_DOWN: rect.y -= 10;
                        break;
        case SDLK_RIGHT: rect.x -= 10;
                        break;
        case SDLK_LEFT: rect.x += 10;
                        break;
      }

    }

    else if(e.type == SDL_MOUSEBUTTONDOWN){

      if(e.button.button == SDL_BUTTON_LEFT){
        rect.x=0;rect.y=0;
      }

    }
    SDL_FillRect(d->screen, NULL, SDL_MapRGB(d->screen->format, 0xFF, 0xFF, 0xFF));
    SDL_BlitSurface(image, &rect, d->screen, NULL);
    SDL_UpdateWindowSurface(d->window);
    }

  end(d, image);

  return 0;
}

struct Display* init(){

  struct Display* back;
  back = new Display;

  SDL_Init(SDL_INIT_VIDEO);
  IMG_Init(IMG_INIT_PNG);

  back->window = SDL_CreateWindow("Test", 400, 400, 800, 800, SDL_WINDOW_SHOWN);
  SDL_SetWindowFullscreen(back->window, SDL_WINDOW_FULLSCREEN_DESKTOP);
  back->screen = SDL_GetWindowSurface(back->window);

  return back;


}


void end(struct Display* d, SDL_Surface* img){
  SDL_FreeSurface(img);
  SDL_DestroyWindow(d->window);
  SDL_Quit();
}
