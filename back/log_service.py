import pickle
import logging

file_name = "history_data.pkl"


def write_to_file(players_connected,diction_games):
    with open(file_name, 'wb') as handle:
        pickle.dump(players_connected, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(diction_games, handle, protocol=pickle.HIGHEST_PROTOCOL)
    add_log_info("\tlog_service, write_to_file: Wrote data to" + file_name + " successfully")

def define_log_file_output(filename='example.log'):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename, 'w', 'utf-8')
    root_logger.addHandler(handler)


def add_log_warnning(msg):
    logging.warning("[FAIL]" + msg)


def add_log_info(msg):
    logging.info(msg)


def load_from_file():
    try:
        with open(file_name, 'rb') as handle:
            players_connected = pickle.load(handle)
            diction_games = pickle.load(handle)
        id_count = len(players_connected['id'])
        # file.close()
        add_log_info("\tlog_service, load_from_file: data loaded successfully.")
        return players_connected, diction_games, id_count
    except FileNotFoundError:
        add_log_info("\tlog_service, load_from_file: File history_data.pkl does not exits.")
    return {'id': []}, {}, 0
