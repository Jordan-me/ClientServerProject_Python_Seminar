import PySimpleGUI as sg
import webbrowser


class server_gui():
    def __init__(self, player1_id, player2_id):
        server_gui.player1_id = player1_id
        server_gui.player2_id = player2_id

        sg.theme('DarkAmber')
        layout = [[[sg.Text('Player 1 :'), sg.Text(server_gui.player1_id, key='p1_id', visible=True)],
                  [sg.Text('Player 2 :'), sg.Text(server_gui.player2_id, key='p2_id', visible=True)]],
                  [sg.Text('Select jar file :'), sg.InputText(), sg.FileBrowse()],
                  [sg.Text('Server folder  :'), sg.InputText(key='-fd-'), sg.FolderBrowse()],
                  [sg.Checkbox('Accept Eula', default=False, key='-ae-'), sg.Checkbox('Open readme', default=True, key='-wb-')],
                  [sg.Submit(), sg.Button('Close')]]

        server_gui.window = sg.Window('Setup', layout, icon=r'images\Luxury_Logo (2).ico')

        while True:
            event, values = server_gui.window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
        server_gui.window.close()

        b = open(f"{values['-fd-']}/start.bat", 'w')
        mr = [f"java -Xmx{values[0]}M -Xms{values[1]}M -jar {values[2]} nogui\n", "pause"]
        b.writelines(mr)
        b.close()

        e = open(f"{values['-fd-']}/eula.txt", "w")
        e.write(f"eula={values['-ae-']}")

        e.close()

        if values['-wb-']:
            webbrowser.open("readme.txt")
    def setPlayers( id1, id2):
        print("setting new window", server_gui.window.layout)
        server_gui.player1_id = id1
        server_gui.player2_id = id2
        print(server_gui.player1_id, server_gui.player2_id)
        # server_gui.window['']
        server_gui.window['p1_id'].Update(server_gui.player1_id)
        server_gui.window['p2_id'].Update(server_gui.player2_id)
        #
        # layout = [[sg.Text('Player 1 :'), sg.Text(server_gui.player1_id)],
        #           [sg.Text('Player 2 :'), sg.Text(server_gui.player2_id)],
        #           [sg.Text('Select jar file :'), sg.InputText(), sg.FileBrowse()],
        #           [sg.Text('Server folder  :'), sg.InputText(key='-fd-'), sg.FolderBrowse()],
        #           [sg.Checkbox('Accept Eula', default=False, key='-ae-'),
        #            sg.Checkbox('Open readme', default=True, key='-wb-')],
        #           [sg.Submit(), sg.Button('Close')]]
        # server_gui.window.refresh()
        # server_gui.window = sg.Window('Setup', layout, icon=r'images\Luxury_Logo (2).ico')



