from ._anvil_designer import BrailleConnectTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

global tobraille
tobraille = {
  "a": "⠁",
  "b": "⠃",
  "c": "⠉",
  "d": "⠙",
  "e": "⠑",
  "f": "⠋",
  "g": "⠛",
  "h": "⠓",
  "i": "⠊",
  "j": "⠚",
  "k": "⠅",
  "l": "⠇",
  "m": "⠍",
  "n": "⠝",
  "o": "⠕",
  "p": "⠏",
  "q": "⠟",
  "r": "⠗",
  "s": "⠎",
  "t": "⠞",
  "u": "⠥",
  "v": "⠧",
  "w": "⠺",
  "x": "⠭",
  "y": "⠽",
  "z": "⠵",
  "1": "⠁",
  "2": "⠃",
  "3": "⠉",
  "4": "⠙",
  "5": "⠑",
  "6": "⠋",
  "7": "⠛",
  "8": "⠓",
  "9": "⠊",
  "0": "⠚",
  ",": "⠂",
  ";": "⠆",
  ":": "⠒",
  "?": "⠦",
  "!": "⠖",
  "'": "⠄",
  '"': "⠦",
  "(": "⠶",
  ")": "⠶",
  "-": "⠤",
  "/": "⠸⠌",
  "\\": "⠸⠡",
  "&": "⠯",
  "#": "⠸⠹",
  ".": "⠲",
  "|": "⠸⠳",
  "+": "⠐⠖",
  "=": "⠐⠶",
  "%": "⠨⠴",
  "@": "⠈⠁",
  " ": " ",
  "": "",
  "with": "⠾",
  "and": "⠯",
  "for": "⠿",
  "the": "⠮",
  "ing": "⠬",
  "of": "⠷",
  "ch": "⠡",
  "gh": "⠣",
  "sh": "⠩",
  "st": "⠌",
  "th": "⠹",
  "wh": "⠱",
  "ed": "⠫",
  "er": "⠻",
  "ou": "⠳",
  "ow": "⠪",
  "in": "⠔",
}

global selectlang
selectlang = "en"
languages = {
  "Spanish": "es",
  "French": "fr",
  "Japanese": "ja",
  "Chinese": "zh",
  "Dutch": "nl",
  "Hindi": "hi",
  "Italian": "it",
  "Russian": "ru",
  "Bengali": "bn",
  "Swedish": "sv",
  "Thai": "th",
  "Urdu": "ur",
  "German": "de",
  "Javanese": "jv",
  "Korean": "ko",
  "Portuguese": "pt",
  "Arabic": "ar",
  "Vietnamese": "vi",
  "Turkish": "tr",
}


def to_braille(txt):
  skip = 0
  brailletxt = ""
  num = False
  caps = False
  for i in range(0, len(txt)):
    if skip > 0:
      skip -= 1
      continue
    elif txt[i : i + 1] == "\n":
      brailletxt += "\n"
      num = False
      continue

    if txt[i].isupper() is True:
      if caps is False:
        if len(txt) - 1 == i or txt[i + 1].isupper() is False:
          brailletxt += "⠠"
        else:
          brailletxt += "⠠⠠"
          caps = True
    else:
      if caps is True:
        caps = False
        brailletxt += "⠠⠄"

    if txt[i : i + 4].lower() in ["with"]:
      if num is True:
        num = False
      skip = 3
      brailletxt += tobraille[txt[i : i + 4].lower()]
    elif txt[i : i + 3].lower() in ["and", "for", "the", "ing"]:
      if num is True:
        num = False
      skip = 2
      brailletxt += tobraille[txt[i : i + 3].lower()]
    elif txt[i : i + 2].lower() in [
      "of",
      "ch",
      "gh",
      "sh",
      "st",
      "th",
      "wh",
      "ed",
      "er",
      "ou",
      "ow",
      "in",
    ]:
      if num is True:
        num = False
      skip = 1
      brailletxt += tobraille[txt[i : i + 2].lower()]
    elif txt[i] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
      if num is False:
        brailletxt += "⠼"
        num = True
      brailletxt += tobraille[txt[i]]
    elif txt[i] in ["."]:
      brailletxt += tobraille[txt[i]]
    elif txt[i].lower() in tobraille:
      if txt[i] in " ,-;:?!'\\\"()#&/":
        num = False
      else:
        if num is True:
          num = False
          brailletxt += "⠰"
      brailletxt += tobraille[txt[i].lower()]
    else:
      brailletxt += "□"
  if caps is True:
    brailletxt += "⠠⠄"
  return brailletxt


class BrailleConnect(BrailleConnectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def home_click(self, **event_args):
    open_form("Home")
  def BrailleConnect_click(self, **event_args):
    open_form("BrailleConnect")

  def frombraille_click(self, **event_args):
    open_form("FromBraille")

  def tobraille_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def pharma_click(self, **event_args):
    c = Link(
      url="https://www.pharmabraille.com/pharmaceutical-braille/the-braille-alphabet/"
    )
    self.add_component(c)

  def info_click(self, **event_args):
    open_form("Info")

  def i_use_click(self, **event_args):
    self.infobox.visible = True
    self.crossinfo.visible = True
    self.convert.visible = False
    self.textbox.visible = False
    self.braillebox.visible = False
    self.i_use.visible = False
    self.selectmsg.visible = False
    self.lang.visible = False

  def crossinfo_click(self, **event_args):
    self.infobox.visible = False
    self.crossinfo.visible = False
    self.convert.visible = True
    self.textbox.visible = True
    self.braillebox.visible = True
    self.i_use.visible = True
    self.selectmsg.visible = True
    self.lang.visible = True

  def convert_click(self, **event_args):
    if selectlang == "en":
      self.braillebox.text = to_braille(self.textbox.text)
    else:
      box_txt = self.textbox.text
      finaltxt = anvil.server.call("translang", selectlang, box_txt)
      print(finaltxt)
      self.braillebox.text = to_braille(finaltxt)

  def lang_change(self, **event_args):
    global selectlang
    selectlang = languages[self.lang.selected_value]

  ##############################################

  def braillebox_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass
