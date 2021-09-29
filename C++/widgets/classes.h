// base.h
#ifndef BASIC_H
#define BASIC_H
// Für die Ereignis-Handles
enum {
MENU_FILE_QUIT,
ID_FRAME
};
class wxDialogDemoApp : public wxApp {
public: virtual bool OnInit();
};
class BasicFrame : public wxFrame {
private:
wxMenuBar *MenuBar;
wxMenu *ExampleMenu;
wxNotebook* notebook;
// Ereignis-Tabelle einrichten
DECLARE_EVENT_TABLE()
public:
BasicFrame( const wxChar *title,
int xpos, int ypos,
int width, int height);
~BasicFrame();
// Methoden, die auf Ereignisse reagieren
void OnMenuFileQuit(wxCommandEvent &event);
void OnScrolledWindow( wxScrollWinEvent& event );
};
class MyScrolledWindow : public wxScrolledWindow {
private:
DECLARE_EVENT_TABLE()
public:
MyScrolledWindow( wxWindow* parent, wxWindowID id,
int xpos, int ypos,
int width, int height,
long style, int pixelPerUnitX,
int pixelPerUNIXY, int noUnitsX,
int noUnitsY, bool refresh );
~MyScrolledWindow();
void OnScrolledWindow(wxScrollWinEvent& event );
};
#endif
