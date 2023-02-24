from dialogs import SambaServer
from yast import import_module
import_module('Wizard')
import_module('UI')
import_module('Sequencer')
from yast import Wizard, UI, Sequencer, Symbol

def Sequence():
    aliases = {
        'samba-server' : [(lambda: SambaServer().Show())],
    }

    sequence = {
        'ws_start' : 'samba-server',
        'samba-server' : {
            Symbol('abort') : Symbol('abort'),
            Symbol('next') : Symbol('next'),
        },
    }

    Wizard.CreateDialog()
    Wizard.SetTitleIcon('yast-samba-server')

    ret = Sequencer.Run(aliases, sequence)

    UI.CloseDialog()
    return ret

