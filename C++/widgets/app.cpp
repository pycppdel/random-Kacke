// base.cpp
#include <wx/wx.h>
#include <wx/notebook.h>
#include "classes.h"
IMPLEMENT_APP(wxDialogDemoApp)
bool wxDialogDemoApp::OnInit() {
BasicFrame *frame =
new BasicFrame( wxT("Demonstriert wxScrollbar"),
50, 50, 400, 300 );
frame->Show(TRUE);
SetTopWindow(frame);
return TRUE;
}
BasicFrame::BasicFrame (
const wxChar *title,
int xpos, int ypos,

int width, int height)
: wxFrame ( (wxFrame *) NULL,
ID_FRAME, title,
wxPoint(xpos, ypos),
wxSize(width, height),wxDEFAULT_FRAME_STYLE)
{
// Eine Menübar erzeugen
MenuBar = new wxMenuBar();
// Ein Menü erzeugen
ExampleMenu = new wxMenu();
ExampleMenu->Append(MENU_FILE_QUIT, wxT("&Beenden"));
MenuBar->Append( ExampleMenu, wxT("&Datei"));
SetMenuBar(MenuBar);
// Ein Notebook erzeugen
notebook = new wxNotebook(
this, wxID_ANY, wxDefaultPosition, wxSize(300, 200));
// Ein Fenster zum Scrollen nur in vertikaler Richtung
MyScrolledWindow *window1 = new MyScrolledWindow(notebook, wxID_ANY, 0, 0, 1, 1,wxVSCROLL, 0, 10, 0, 500, true );
// Einen Button hinzufügen
(void) new wxButton( window1, wxID_ANY, wxT("Button1"),
wxPoint(10, 10), wxDefaultSize );
// Ein Fenster zum Scrollen nur in horizontaler Richtung
MyScrolledWindow *window2 = new MyScrolledWindow(
notebook, wxID_ANY, 0, 0, 1, 1,
wxHSCROLL, 10, 0, 500, 0, true );
// Einen Button hinzufügen
(void) new wxButton(window2 , wxID_ANY, wxT("Button2"),
wxPoint(10, 10), wxDefaultSize );
// Ein Fenster zum Scrollen in beide Richtungen
MyScrolledWindow *window3 = new MyScrolledWindow(
notebook, wxID_ANY, 0, 0, 1, 1,
wxHSCROLL|wxVSCROLL, 10, 10, 500, 500, true );
// Einen Button hinzufügen
(void) new wxButton(window3, wxID_ANY, wxT("Button3"),
wxPoint(10, 10), wxDefaultSize );
// ... und zum Notebook hinzufügen
notebook->AddPage(
window1, wxT("Vertikal Scroll"), true );
notebook->AddPage(
window2, wxT("Horizontal Scroll"), false);
notebook->AddPage(

window3, wxT("Vertikal und Horizontal"), false);
// Eine Statusleiste
CreateStatusBar(1);
}
BasicFrame::~BasicFrame() { }
// Ereignis-Tabelle für das Frame
BEGIN_EVENT_TABLE(BasicFrame, wxFrame)
EVT_MENU(MENU_FILE_QUIT, BasicFrame::OnMenuFileQuit)
END_EVENT_TABLE()
void BasicFrame::OnMenuFileQuit(wxCommandEvent &event) {
Destroy();
}
MyScrolledWindow::MyScrolledWindow(
wxWindow* parent, wxWindowID id,
int xpos, int ypos,
int width, int height,
long style, int pixelPerUnitX,
int pixelPerUnitY, int noUnitsX,
int noUnitsY, bool refresh ):
wxScrolledWindow( parent, id, wxPoint(xpos, ypos),
wxSize(width, height), style )
{
SetScrollbars( pixelPerUnitX, pixelPerUnitY,
noUnitsX, noUnitsY,
0, 0, refresh );
}
MyScrolledWindow::~MyScrolledWindow() {}
void MyScrolledWindow::OnScrolledWindow(
wxScrollWinEvent& event ) {
// Um die Statuszeile nutzen zu können, benötigen wir
// einen Weg, um darauf zuzugreifen
// (siehe wxWindow::FindWindowbyID)
wxFrame* win = (wxFrame*) FindWindowById(ID_FRAME, NULL);
// wurde vertikal gescrollt
// siehe auch wxScrollWinEvent::GetOrientation
if( event.GetOrientation() == wxVERTICAL )
win->SetStatusText(
wxT("Scrollbar vertikal betätigt") );
}
