import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import translate
from translate import Translator

# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def translang(fromlang, txt):
  translation = Translator(from_lang=fromlang,to_lang="en").translate(txt)
  return translation
  
@anvil.server.callable
def transeng(tolang, txt):
  translation = Translator(from_lang="en",to_lang=tolang).translate(txt)
  return translation
