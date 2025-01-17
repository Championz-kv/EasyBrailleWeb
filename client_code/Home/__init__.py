from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    

    # Any code you write here will run before the form opens.
    
  def home_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
  def info_click(self, **event_args):
    open_form('Info')
  def frombraille_click(self, **event_args):
    open_form("FromBraille")
  def tobraille_click(self, **event_args):
    open_form("ToBraille")
  def pharma_click(self, **event_args):
    c = Link(url="https://www.pharmabraille.com/pharmaceutical-braille/the-braille-alphabet/")
    self.add_component(c)
###############################################
  def outlined_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass




