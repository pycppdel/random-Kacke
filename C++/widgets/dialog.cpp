#include <wx/wx.h>
#include <wx/spinbutt.h>
#include <wx/stattext.h>
#include <wx/notebook.h>
#include <wx/bitmap.h>
#include <iostream>

class App;
class PFrame;
class Dia;

class App: public wxApp{

public:

  bool OnInit();

};

IMPLEMENT_APP(App);

class PFrame: public wxMDIParentFrame{

public:

  wxMenuBar* menu;
  wxMenu* men;
  Dia* d;
  wxStaticText* text;
  wxBitmap* map;
  wxStaticBitmap* img;


  enum actions{

    SHOW_DIALOG

  };

  PFrame();
  ~PFrame();

  void make_menu_bar();
  void onDialog(wxCommandEvent& evt);

  DECLARE_EVENT_TABLE()
};

class Dia: public wxDialog{


public:

  wxButton* but;

  Dia();
  ~Dia();

  void onClose(wxCloseEvent& evt);
  DECLARE_EVENT_TABLE()
};




//DEF
bool App::OnInit(){

PFrame* frame = new PFrame();
SetTopWindow(frame);
std::cout << "\a";
return TRUE;

}


PFrame::PFrame():
wxMDIParentFrame((wxMDIParentFrame*)NULL, 1, wxT("Hallo Welt"), wxPoint(950, 500), wxSize(600, 600))
{

  make_menu_bar();

Show(true);

}

PFrame::~PFrame(){

}

void PFrame::make_menu_bar(){


  menu = new wxMenuBar();
  men = new wxMenu();
  men->Append(actions::SHOW_DIALOG, wxT("show dialog"));
  menu->Append(men, wxT("Dialog"));
  text = new wxStaticText(this, 56, wxT("SPIN"), wxPoint(450, 400), wxSize(100, 100));
  map = new wxBitmap(wxT("skull.bmp"));
  img = new wxStaticBitmap(this, 66, *map, wxPoint(88, 99));
  SetMenuBar(menu);


}
void PFrame::onDialog(wxCommandEvent& evt){

d = new Dia();

}

Dia::Dia():
wxDialog((wxWindow*)NULL,  2, wxT("DIALOG"), wxPoint(200, 200), wxSize(400, 400))
{
  but = new wxButton(this, wxID_OK, wxT("Ok"), wxPoint(300, 300), wxSize(600,600));
  ShowModal();

}

Dia::~Dia(){

}

void Dia::onClose(wxCloseEvent& evt){

  Destroy();
}

BEGIN_EVENT_TABLE(PFrame, wxFrame)
EVT_MENU(actions::SHOW_DIALOG, PFrame::onDialog)
END_EVENT_TABLE()

BEGIN_EVENT_TABLE(Dia, wxDialog)
EVT_CLOSE( Dia::onClose)
END_EVENT_TABLE()
