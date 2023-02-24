from yast import import_module
import_module('Wizard')
import_module('UI')
from yast import *
from subprocess import Popen, PIPE

def wait_event():
    event = UI.WaitForEvent()
    if 'WidgetID' in event:
        ret = event['WidgetID']
    elif 'ID' in event:
        ret = event['ID']
    else:
        raise Exception('ID not found in response %s' % str(event))
    return ret

def UpdateUI(p):
    msg = 'Updating the samba-server image... '
    UI.OpenDialog(
        MinWidth(42, VBox(
            Left(Label(Id('status'), msg)),
            LogView(Id('output'), '', 5, 0),
            ReplacePoint(Id('close_btn'), PushButton(Opt('disabled'), "&OK"))
        ))
    )
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            UI.ChangeWidget(Id('output'), Symbol('LastLine'), line)
    ret = p.wait()
    if ret == 0:
        UI.ChangeWidget(Id('status'), 'Value', msg+'Success')
    else:
        UI.ChangeWidget(Id('status'), 'Value', msg+'Failed')
    UI.ReplaceWidget(Id('close_btn'), PushButton(Id('close'), "&OK"))
    while True:
        ret = wait_event()
        if ret == 'close':
            UI.CloseDialog()
            break
    return ret

class SambaPodman():
    samba_server_image = 'registry.opensuse.org/opensuse/samba-server'
    def __init__(self):
        pass

    def update(self):
        # Update the samba-server image
        p = Popen(['podman', 'pull', self.samba_server_image],
                  stdout=PIPE, stderr=PIPE)
        return UpdateUI(p)

    def running(self):
        # Check if the container is running
        out, err = Popen(['podman', 'ps', '--format', '{{.Image}}'],
                         stdout=PIPE, stderr=PIPE).communicate()
        for image in out.split('\n'):
            if self.samba_server_image in image:
                return True
        return False

    def present(self):
        # Check if the image is present
        out, err = Popen(['podman', 'image', 'list', '--filter',
                          'reference=%s' % self.samba_server_image], 
                         stdout=PIPE, stderr=PIPE).communicate()
        if self.samba_server_image in out:
            return True
        return False

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

title = 'Samba Containerized Server'

def DeleteButtonBox():
    '''Hide the Wizard button box from the bottom of the window
    '''
    Wizard.HideBackButton()
    Wizard.HideNextButton()
    Wizard.HideAbortButton()
    if UI.WidgetExists(Id('rep_help')):
        UI.ReplaceWidget(Id('rep_help'), Empty())

class SambaServer():
    def __init__(self):
        self.pclient = SambaPodman()

    def Show(self):
        UI.SetApplicationTitle(title)
        Wizard.SetContentsButtons('', self.main_dialog(), '', '', '')
        UI.ReplaceWidget(Id('tabpane'), self.startup())
        DeleteButtonBox()
        UI.SetFocus('startup')
        while True:
            ret = wait_event()
            if ret == 'abort' or ret == 'cancel':
                break
            elif ret == 'startup':
                UI.ReplaceWidget(Id('tabpane'), self.startup())
            elif ret == 'shares':
                UI.ReplaceWidget(Id('tabpane'), self.shares())
            elif ret == 'identity':
                UI.ReplaceWidget(Id('tabpane'), self.identity())
            elif ret == 'trusted_domains':
                UI.ReplaceWidget(Id('tabpane'), self.trusted_domains())
            elif ret == 'ldap_settings':
                UI.ReplaceWidget(Id('tabpane'), self.ldap_settings())
            elif ret == 'container_restart':
                pass
            elif ret == 'container_start':
                pass
            elif ret == 'update_container':
                self.pclient.update()
            UI.SetApplicationTitle(title)
        return Symbol(ret)

    def main_dialog(self):
        return HBox(VBox(DumbTab(
            [
                Item(Id('startup'), 'Start-Up'),
                Item(Id('shares'), 'Shares'),
                Item(Id('identity'), 'Identity'),
                Item(Id('trusted_domains'), 'Trusted Domains'),
                Item(Id('ldap_settings'), 'LDAP Settings')
            ],
            ReplacePoint(Id('tabpane'), Empty())
        ), VStretch()), HStretch())

    def fetch_container_state(self):
        return 'Inactive'

    def startup(self):
        state = self.fetch_container_state()
        btn_action = 'Restart' if state == 'Active' else 'Start'
        return VBox(
            Frame('Container Configuration',
                Label('Current status: %s' % state)
            ),
            PushButton(Id('update_container'), 'Update Container'),
            ReplacePoint(Id('statebtn'), PushButton(Id('container_%s' % btn_action.lower()), btn_action)),
            Frame('Firewall Settings for firewalld', Empty())
        )

    def shares(self):
        return Empty()
    
    def identity(self):
        return Empty()

    def trusted_domains(self):
        return Empty()

    def ldap_settings(self):
        return Empty()
