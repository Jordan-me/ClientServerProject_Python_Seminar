import sys

from back.log_service import define_log_file_output
from front.serverGui import ServerGui

if __name__ == "__main__":
    define_log_file_output(filename='logger.log')
    server_window = ServerGui(argv=sys.argv)
    sys.exit(server_window.app.exec_())
