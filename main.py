# Alogirthm
import method.rsa as rsa
import method.elgamal as eg
import method.paillier as pl
import method.ecc as ecc

# GUI
import PySimpleGUI as sg

def RSA_GUI():
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
            if values['option'] == 'Affine':
                RSA_GUI()
            elif values['option'] == 'Playfair':
                ElGamal_GUI()
            elif values['option'] == 'Vigenere':
                Paillier_GUI()
            elif values['option'] == 'Vigenere Auto-Key':
                ECC_GUI()
    window.close()

if __name__ == '__main__':
    main()