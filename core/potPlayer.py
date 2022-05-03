import win32gui
import win32con    

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        windowTitle = win32gui.GetWindowText( hwnd )
        isVLCWindow = windowTitle.find(ctx) > -1
        if isVLCWindow:
            win32gui.SetForegroundWindow(hwnd)

def winEnumCloseHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        windowTitle = win32gui.GetWindowText( hwnd )
        isVLCWindow = windowTitle.find(ctx) > -1
        if isVLCWindow:
            win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)

def closePotPlayer():
    win32gui.EnumWindows( winEnumCloseHandler, 'PotPlayer' )

def focusPotPlayer():
    win32gui.EnumWindows( winEnumHandler, 'PotPlayer' )
