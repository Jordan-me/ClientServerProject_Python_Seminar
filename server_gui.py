import PySimpleGUI as sg
import webbrowser

layout = []


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

        ]

        server_gui.window = sg.Window('Setup', layout, icon=r'images\Luxury_Logo (2).ico')

        while True:
            event, values = server_gui.window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
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

        print("details: "+str(server_gui.gameIds))

        print("layout: "+str(layout))
        server_gui.player1_id = id1
        server_gui.player2_id = id2
        print(server_gui.player1_id, server_gui.player2_id)
        # server_gui.window['']
        server_gui.window['p1_id'].Update(server_gui.player1_id)
        server_gui.window['p2_id'].Update(server_gui.player2_id)
        if id1 != 0 and id2 != 0:
            server_gui.games.append("Game " + str(gameId) + " : " + str(server_gui.gameIds[gameId]) + "\n")
            games_str = get_games_str(server_gui.games)
            print("games str: \n" + games_str)
            server_gui.window['games_played'].Update(games_str)
        print(server_gui.gameIds[gameId])





