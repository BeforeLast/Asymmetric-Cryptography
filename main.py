# Alogirthm
from PySimpleGUI.PySimpleGUI import Save
import method.rsa as rsa
import method.elgamal as eg
import method.paillier as pl
import method.ecc as ecc

# GUI
import PySimpleGUI as sg

def RSA_GUI():
    layout = [
        [sg.Text('Text :'),sg.InputText(key='text')],
        [sg.Text('n = '),sg.InputText(key='n',default_text='0')],
        [sg.Text('e = '),sg.InputText(key='e',default_text='0')],
        [sg.Text('d = '),sg.InputText(key='d',default_text='0')],
        [sg.Button('Generate Key'),sg.Checkbox('Save to file',key='save')],
        [sg.Button('Import Public Key'),sg.InputText(default_text='./key/rsa_key.pub',disabled=True,key='imp_pub'),sg.FileBrowse(initial_folder='./key/', file_types=(("Public Key Files","*.pub"),))],
        [sg.Button('Import Private Key'),sg.InputText(default_text='./key/rsa_key.pri',disabled=True,key='imp_pri'),sg.FileBrowse(initial_folder='./key/', file_types=(("Private Key Files","*.pri"),))],
        [sg.Button('Encrypt'),sg.Button('Decrypt')],
        [sg.Multiline(size=(100,60),disabled=True,key='res')]
    ]
    window = sg.Window(title=('RSA'), layout=layout, size=(700,800), modal=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        res = ''
        pub_key = {'n':int(values['n']),'e':int(values['e'])}
        pri_key = {'n':int(values['n']),'d':int(values['d'])}
        tools = rsa.RSA(pub_key,pri_key)
        if event == 'Generate Key':
            if values['save']:
                tn, te, td = tools.generate_pair(True)
            else:
                tn, te, td = tools.generate_pair(False)
            window.Element(key='n').Update(tn)
            window.Element(key='e').Update(te)
            window.Element(key='d').Update(td)
        elif event == 'Import Public Key':
            key = tools.open_key(values['imp_pub'])
            window.Element(key='n').Update(key['n'])
            window.Element(key='e').Update(key['e'])
        elif event == 'Import Private Key':
            key = tools.open_key(values['imp_pri'])
            window.Element(key='n').Update(key['n'])
            window.Element(key='d').Update(key['d'])
        elif event == 'Encrypt' and len(values['text'])>0:
            transformed_text = bytearray(values['text'].encode())
            ciphertext = tools.encrypt(transformed_text)
            res = ''.join('{:02x}'.format(byte) for byte in ciphertext)
        elif event == 'Decrypt' and len(values['text'])>0:
            try:
                transformed_text = bytearray.fromhex(values['text'])
                plaintext = tools.decrypt(transformed_text)
                res = plaintext.decode('utf-8')
            except:
                res = 'Wrong ciphertext code'
        window.Element(key='res').Update(res)
    pass

def ElGamal_GUI():
    pass

def Paillier_GUI():
    pass

def ECC_GUI():
    pass

def main():
    TOOLS = ['RSA','ElGamal','Paillier','ECC']
    LAYOUT = [
        [sg.Text('Pick Tools :'),sg.OptionMenu(values=TOOLS,default_value='RSA',key='option'),sg.Button('Pick')]
    ]

    window = sg.Window('Asymmetric Cryptography Tools', layout=LAYOUT, size=(250,50))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event=='Pick':
            if values['option'] == 'RSA':
                RSA_GUI()
            elif values['option'] == 'ElGamal':
                ElGamal_GUI()
            elif values['option'] == 'Paillier':
                Paillier_GUI()
            elif values['option'] == 'ECC':
                ECC_GUI()
    window.close()

if __name__ == '__main__':
    main()