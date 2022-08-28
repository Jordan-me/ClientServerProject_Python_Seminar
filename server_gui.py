
import PySimpleGUI as sg
import webbrowser

layout = []


# import PySimpleGUI as sg
#
# def new_layout(i):
#     return [[sg.T("Question: "), sg.InputText(key=("-q-", i)), sg.T("Answer"), sg.InputText(key=("-ans-", i))]]
#
# PLUS_ICO = b'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'
#
# category_list = ("General", "Networking", "Socket 1", "Socket 2", "Socket 3", "Socket 4")
#
# column_layout = [
#     [sg.T("Question: "), sg.InputText(key=("-q-", 0)), sg.T("Answer"), sg.InputText(key=("-ans-", 0)), sg.Button(enable_events=True, image_data=PLUS_ICO, key="-plus-")]
# ]
#
# layout = [
#     [sg.T("Category: "), sg.Combo(values=category_list, size=(15, len(category_list)), default_value="General", key="-cat-", enable_events=True),sg.T("Tag: "), sg.InputText(size=(10,1), key="-t-")],
#     [sg.Column(column_layout, key='-Column-')],
#     [sg.Submit(button_text="Update/Insert"), sg.Cancel(button_text="Cancel")],
# ]
#
# window = sg.Window('Question Taker', layout)
# i = 1
# while True:
#     event, values = window.read()
#     if event in (sg.WIN_CLOSED, 'Exit', 'Cancel'):
#         break
#     elif event == '-plus-':
#         if i<5:
#             window.extend_layout(window['-Column-'], new_layout(i))
#             i += 1
#     print(event, values)
#
# event, values = window.read()
# window.close()
def new_layout(i):
    return [[sg.T("Question: "), sg.Button(key=("-q-", i)), sg.T("Answer"), sg.InputText(key=("-ans-", i))]]

def delete_game_button(p1, p2, gameId):
    # (
    #         "Game " + str(gameId) + ":\tplayer 1 : " + str(game_details[0]) + " vs player 2 : " + str(
    #     game_details[1]) + "     \n")
    return [[sg.Text("Game " + str(gameId) + ":\tplayer 1 : " + str(p1) + " vs player 2 : " + str(p2)),
             sg.Button("Stop game", key="db")]]


def get_games_str(games):
    returnedStr = ""
    for i in games:
        returnedStr += str(i)
    return returnedStr


class server_gui():
    def __init__(self, player1_id, player2_id, gameId):
        server_gui.player1_id = player1_id
        server_gui.player2_id = player2_id
        server_gui.gameIds = {}
        server_gui.games = []

        sg.theme('DarkAmber')
        layout = [
            [sg.Text('Player 1 :'), sg.Text(server_gui.player1_id, key='p1_id', visible=True)],
            [sg.Text('Player 2 :'), sg.Text(server_gui.player2_id, key='p2_id', visible=True)],
            [sg.Text('Games Played :'), sg.Text(0, key='games_played', visible=True)],
            [sg.Button('Exit', key="q", button_color=('white', 'firebrick3'))]

        ]

        server_gui.window = sg.Window('Setup', text_justification='l', default_element_size=(15, 1), font='Any 14',
                                      icon=r'images\Luxury_Logo (2).ico').Layout(layout)

        while True:
            event, values = server_gui.window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
            elif event == 'q':
                server_gui.window.extend_layout(server_gui.window['games_played'], new_layout("delete"))
        server_gui.window.close()

        # b = open(f"{values['-fd-']}/start.bat", 'w')
        # mr = [f"java -Xmx{values[0]}M -Xms{values[1]}M -jar {values[2]} nogui\n", "pause"]
        # b.writelines(mr)
        # b.close()

        # e = open(f"{values['-fd-']}/eula.txt", "w")
        # e.write(f"eula={values['-ae-']}")

        # e.close()

        # if values['-wb-']:
        #     webbrowser.open("readme.txt")

    def setPlayers(id1, id2, gameId):
        print("setting new window", server_gui.window.layout)
        server_gui.gameIds[gameId] = [id1, id2]

        print("details: " + str(server_gui.gameIds))

        print("layout: " + str(layout))
        server_gui.player1_id = id1
        server_gui.player2_id = id2
        print(server_gui.player1_id, server_gui.player2_id)
        # server_gui.window['']
        server_gui.window['p1_id'].Update(server_gui.player1_id)
        server_gui.window['p2_id'].Update(server_gui.player2_id)
        if id1 != 0 and id2 != 0:
            game_details = server_gui.gameIds[gameId]
            server_gui.window.extend_layout(server_gui.window['games_played'], delete_game_button(game_details[0], game_details[1], gameId))
            # server_gui.games.append(
            #     "Game " + str(gameId) + ":\tplayer 1 : " + str(game_details[0]) + " vs player 2 : " + str(
            #         game_details[1]) + "     \n")
            # games_str = get_games_str(server_gui.games)
            # print("games str: \n" + games_str)
            # server_gui.window['games_played'].Update(games_str)
        print(server_gui.gameIds[gameId])