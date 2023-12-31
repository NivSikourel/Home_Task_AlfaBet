import threading
from http.server import HTTPServer

from DataBase import create_table
from EventHandler import EventHandler
from ReminderUtilities import scheduler


def stop_server():
    httpd.shutdown()


def run(server_class=HTTPServer, handler_class=EventHandler, port=8080):
    create_table()
    server_address = ('', port)
    global httpd
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')

    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=scheduler.run)
    scheduler_thread.start()

    httpd.serve_forever()


if __name__ == '__main__':
    run()
