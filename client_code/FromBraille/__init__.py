from ._anvil_designer import FromBrailleTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

brailles = { "1" : "⠁", 
"2" : "⠂", 
"12" : "⠃", 
"3" : "⠄", 
"13" : "⠅", 
"23" : "⠆", 
"123" : "⠇", 
"4" : "⠈", 
"14" : "⠉", 
"24" : "⠊", 
"124" : "⠋", 
"34" : "⠌", 
"134" : "⠍", 
"234" : "⠎", 
"1234" : "⠏", 
"5" : "⠐", 
"15" : "⠑", 
"25" : "⠒", 
"125" : "⠓", 
"35" : "⠔", 
"135" : "⠕", 
"235" : "⠖", 
"1235" : "⠗", 
"45" : "⠘", 
"145" : "⠙", 
"245" : "⠚", 
"1245" : "⠛", 
"345" : "⠜", 
"1345" : "⠝", 
"2345" : "⠞", 
"12345" : "⠟", 
"6" : "⠠", 
"16" : "⠡", 
"26" : "⠢", 
"126" : "⠣", 
"36" : "⠤", 
"136" : "⠥", 
"236" : "⠦", 
"1236" : "⠧", 
"46" : "⠨", 
"146" : "⠩", 
"246" : "⠪", 
"1246" : "⠫", 
"346" : "⠬", 
"1346" : "⠭", 
"2346" : "⠮", 
"12346" : "⠯", 
"56" : "⠰", 
"156" : "⠱", 
"256" : "⠲", 
"1256" : "⠳", 
"356" : "⠴", 
"1356" : "⠵", 
"2356" : "⠶", 
"12356" : "⠷", 
"456" : "⠸", 
"1456" : "⠹", 
"2456" : "⠺", 
"12456" : "⠻", 
"3456" : "⠼", 
"13456" : "⠽", 
"23456" : "⠾", 
"123456" : "⠿",
"" : " " }
frombraille = {"⠁" : "a", 
"⠃" : "b", 
"⠉" : "c", 
"⠙" : "d", 
"⠑" : "e", 
"⠋" : "f", 
"⠛" : "g", 
"⠓" : "h", 
"⠊" : "i", 
"⠚" : "j", 
"⠅" : "k", 
"⠇" : "l", 
"⠍" : "m", 
"⠝" : "n", 
"⠕" : "o", 
"⠏" : "p", 
"⠟" : "q", 
"⠗" : "r", 
"⠎" : "s", 
"⠞" : "t", 
"⠥" : "u", 
"⠧" : "v", 
"⠺" : "w", 
"⠭" : "x", 
"⠽" : "y", 
"⠵" : "z",
"⠾" : "with", 
"⠯" : "and", 
"⠿" : "for", 
"⠮" : "the", 
"⠬" : "ing", 
"⠷" : "of", 
"⠡" : "ch", 
"⠣" : "gh", 
"⠩" : "sh", 
"⠌" : "st", 
"⠹" : "th", 
"⠱" : "wh", 
"⠫" : "ed", 
"⠻" : "er", 
"⠳" : "ou", 
"⠪" : "ow", 
"⠔" : "in", 
"⠂" : ",", 
"⠆" : ";", 
"⠒" : ":", 
"⠖" : "!", 
"⠄" : "'", 
"⠤" : "-",
"⠲" : ".",
"⠀" : " ",
" " : " " }
frombraillenum = {"⠁" : "1", 
"⠃" : "2", 
"⠉" : "3", 
"⠙" : "4", 
"⠑" : "5", 
"⠋" : "6", 
"⠛" : "7", 
"⠓" : "8", 
"⠊" : "9", 
"⠚" : "0"}

global selectlang
selectlang = "en"
languages = {"Spanish" : "es", 
"French" : "fr", 
"Japanese" : "ja", 
"Chinese" : "zh", 
"Dutch" : "nl", 
"Hindi" : "hi", 
"Italian" : "it", 
"Russian" : "ru", 
"Bengali" : "bn", 
"Swedish" : "sv", 
"Thai" : "th", 
"Urdu" : "ur", 
"German" : "de", 
"Javanese" : "jv", 
"Korean" : "ko", 
"Portuguese" : "pt", 
"Arabic" : "ar", 
"Vietnamese" : "vi", 
"Turkish" : "tr"}

def from_braille(txt) :
    skip = 0
    caps = False
    finaltxt = ""
    capslock = False
    quote = False
    num = False
    bracket = False
    maths = False
    symbol = False
    for i in range(0,len(txt)):
        if skip > 0 :
            skip -= 1
            continue
        elif txt[i] == "\n" :
            finaltxt += "\n"
            num = False
        elif symbol is True :
            if txt[i] == "⠳":#######
                finaltxt += "|"
            elif txt[i] == "⠹":
                finaltxt += "#"
            elif txt[i] == "⠌":
                finaltxt += "/"
            elif txt[i] == "⠡":
                finaltxt += "\\"
            else :
                finaltxt += "□"
            symbol = False
        elif maths is True :
            if txt[i] == "⠖":#######
                finaltxt += "+"
            elif txt[i] == "⠶":
                finaltxt += "="
            else :
                finaltxt += "□"
            maths = False
        elif txt[i:i+2] == "⠠⠄" :
            skip = 1
            capslock = False
        elif txt[i] == "⠠":
            if txt[i:i+2] == "⠠⠠" :
                capslock = True
                skip = 1
            else :
                caps = True
                continue
        elif txt[i] == "⠼" :
            num = True
        elif txt[i] == "⠰" :
            num = False
        elif txt[i] in " ⠤⠄⠆⠒⠖" :
            num = False
            finaltxt += frombraille[txt[i]]
        elif txt[i] == "⠶" :
            if bracket is True :
                finaltxt += "("
                bracket = True
            else:
                finaltxt += ")"
                bracket = False
        elif txt[i] == "⠦" :
            if quote is True :
                finaltxt += "\""
                quote = False
            else :
                if i+1 == len(txt) :
                    if txt[i+1] in frombraille and frombraille[txt[i+1]] == " " :
                        finaltxt += "?"
                else :
                    finaltxt += "\""
                    quote = True 
        elif txt[i] == "⠐" :
            maths = True
        elif txt[i] == "⠸" :
            symbol = True
        elif txt[i:i+2] == "⠨⠴" :
            finaltxt += "%"
            skip = 1
        elif txt[i:i+2] == "⠈⠁" :
            finaltxt += "@"
            skip = 1
        #symbol
        else:
            if num is True :
                if txt[i] in frombraillenum :
                    finaltxt += frombraillenum[txt[i]]
                elif txt[i] in frombraille :
                    num = False
                    if caps is True or capslock is True :
                        finaltxt += frombraille[txt[i]].upper()
                    else : 
                        finaltxt += frombraille[txt[i]]
                else :
                    finaltxt += "□"
            else:
                if txt[i] in frombraille :
                    if caps is True or capslock is True :
                        finaltxt += frombraille[txt[i]].upper()
                    else : 
                        finaltxt += frombraille[txt[i]]
                else :
                    finaltxt += "□"
        caps = False
    return(finaltxt)
global ent_braille
ent_braille = ""

def sortString(a):
    return ''.join(sorted(a))

class FromBraille(FromBrailleTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def home_click(self, **event_args):
    open_form("Home")
  def frombraille_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
  def tobraille_click(self, **event_args):
    open_form("ToBraille")
  def pharma_click(self, **event_args):
    c = Link(url="https://www.pharmabraille.com/pharmaceutical-braille/the-braille-alphabet/")
    self.add_component(c)
  def info_click(self, **event_args):
    open_form("Info")

  def btn1_change(self, **event_args):
    global ent_braille
    if self.btn1.checked is True :
      ent_braille += "1"
    if self.btn1.checked is False :
      ent_braille = ent_braille.replace("1","")
  def btn2_change(self, **event_args):
    global ent_braille
    if self.btn2.checked is True :
      ent_braille += "2"
    if self.btn2.checked is False :
      ent_braille = ent_braille.replace("2","")
  def btn3_change(self, **event_args):
    global ent_braille
    if self.btn3.checked is True :
      ent_braille += "3"
    if self.btn3.checked is False :
      ent_braille = ent_braille.replace("3","")
  def btn4_change(self, **event_args):
    global ent_braille
    if self.btn4.checked is True :
      ent_braille += "4"
    if self.btn4.checked is False :
      ent_braille = ent_braille.replace("4","")
  def btn5_change(self, **event_args):
    global ent_braille
    if self.btn5.checked is True :
      ent_braille += "5"
    if self.btn5.checked is False :
      ent_braille = ent_braille.replace("5","")
  def btn6_change(self, **event_args):
    global ent_braille
    if self.btn6.checked is True :
      ent_braille += "6"
    if self.btn6.checked is False :
      ent_braille = ent_braille.replace("6","")

  def shift_click(self, **event_args):
    global ent_braille
    print(ent_braille,brailles[sortString(ent_braille)])
    self.braillebox.text += brailles[sortString(ent_braille)]
    ent_braille = ""
    self.btn1.checked = False
    self.btn2.checked = False
    self.btn3.checked = False
    self.btn4.checked = False
    self.btn5.checked = False
    self.btn6.checked = False
    
  def backspace_click(self, **event_args):
    self.braillebox.text = self.braillebox.text[0:len(self.braillebox.text)-1]
  def enter_click(self, **event_args):
    self.braillebox.text += "\n"
  def i_use_click(self, **event_args):
    self.infobox.visible = True
    self.crossinfo.visible = True
    self.btn1.visible = False
    self.btn2.visible = False
    self.btn3.visible = False
    self.btn4.visible = False
    self.btn5.visible = False
    self.btn6.visible = False
    self.shift.visible = False
    self.backspace.visible = False
    self.enter.visible = False
    self.i_use.visible = False
    self.braillebox.visible = False
    self.textbox.visible = False
    self.convert.visible = False
    self.translatemsg.visible = False
    self.lang.visible = False
  def crossinfo_click(self, **event_args):
    if self.crossinfo.visible is True :
      self.infobox.visible = False
      self.crossinfo.visible = False
      self.btn1.visible = True
      self.btn2.visible = True
      self.btn3.visible = True
      self.btn4.visible = True
      self.btn5.visible = True
      self.btn6.visible = True
      self.shift.visible = True
      self.backspace.visible = True
      self.enter.visible = True
      self.i_use.visible = True
      self.braillebox.visible = True
      self.textbox.visible = True
      self.convert.visible = True
      self.translatemsg.visible = True
      self.lang.visible = True

  def lang_change(self, **event_args):
    global selectlang
    selectlang = languages[self.lang.selected_value]
  def convert_click(self, **event_args):
    engtxt = from_braille(self.braillebox.text)
    if selectlang == "en":
      self.textbox.text = engtxt
    else:
      finaltxt = anvil.server.call('transeng',selectlang, engtxt)
      self.textbox.text = finaltxt
    
##############################################
