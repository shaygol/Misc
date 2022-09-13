#############################
## (C) Shay Goldshmit 2022 ##
#############################

# public imports
import sys
import time
import random

try:
    import webbrowser
    import threading
    import socket
    from telnetlib import Telnet
    import paramiko
except Exception as e:
    print(f'import error: {e}')
    sys.exit()

IE = webbrowser.get('C:\\Program Files (x86)\\internet explorer\\iexplore.exe')
telnet_sessions_lst = []
ssh_sessions_lst = []
http_sessions_lst = []
https_sessions_lst = []
tcp_sessions_lst = []
all_sess = []
all_session_thread_lst = []
resources_lst = [telnet_sessions_lst, ssh_sessions_lst, http_sessions_lst, https_sessions_lst,
                 tcp_sessions_lst, all_session_thread_lst]
log_err_str = ''
log_err_global_num = 0
is_already_closed = True


def telnet_creation(hostname, user_name=None, password=None, port=23):
    global log_err_str
    global log_err_global_num

    try:
        telnet_connection = Telnet(hostname, port)
        login_log = ''

        if len(user_name) and len(password):
            output = telnet_connection.read_until(b"User Name:")
            login_log = login_log + output.decode('ascii')
            telnet_connection.write(user_name.encode('ascii') + b"\n")

            output = telnet_connection.read_until(b"Password:")
            login_log = login_log + output.decode('ascii')
            telnet_connection.write(password.encode('ascii') + b"\n")

            output = telnet_connection.read_until(b"#")
            login_log = login_log + output.decode('ascii')

            # print(login_log)
    except ConnectionError as e:
        print('telnet_creation | Exception caught[1]: ' + str(e))
        log_err_global_num += 1
        log_err_str += f'{log_err_global_num}) TELNET: {str(e)}\n'
    except Exception as e:
        print('telnet_creation | Exception caught[2]: ' + str(e))
        log_err_global_num += 1
        log_err_str += f'{log_err_global_num}) TELNET: {str(e)}\n'
    else:
        return telnet_connection


def create_telnet_sessions_lst(hostname: str, username=None, password=None, num_of_sessions=0):
    if num_of_sessions == 0:
        return

    global telnet_sessions_lst
    print(f'Generate {num_of_sessions} telnet sessions')

    for i in range(num_of_sessions):
        telnet_sessions_lst.append(telnet_creation(hostname, username, password))


def ssh_creation(hostname, username, password=None, port=22):
    global log_err_str
    global log_err_global_num

    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
    except paramiko.SSHException as e:
        print('ssh_creation | Exception caught[1]: ' + str(e))
        log_err_global_num += 1
        log_err_str += f'{log_err_global_num}) SSH: {str(e)}\n'
    except Exception as e:
        print('ssh_creation | Exception caught[2]: ' + str(e))
        log_err_global_num += 1
        log_err_str += f'{log_err_global_num}) SSH: {str(e)}\n'
    else:
        return ssh


def create_ssh_sessions_lst(hostname: str, username: str, password=None, num_of_sessions=0):
    if num_of_sessions == 0:
        return

    global ssh_sessions_lst
    print(f'Generate {num_of_sessions} SSH sessions')

    for i in range(num_of_sessions):
        ssh_sessions_lst.append(ssh_creation(hostname, username, password))


def socket_creation(hostname, port, stream_type, username=None, password=None):
    global log_err_str
    global log_err_global_num

    try:
        sock = socket.socket(socket.AF_INET, stream_type)
        sock.connect((hostname, port))
    except Exception as e:
        print('socket_creation | Exception caught: ' + str(e))
        log_err_global_num += 1
        stream_type_str = 'TCP' if stream_type == socket.SOCK_STREAM else 'UDP'
        stream_type_str += f'<P_{port}>'
        log_err_str += f'{log_err_global_num}) {stream_type_str}: {str(e)}\n'
    else:
        return sock


def create_tcp_sessions_lst(hostname: str, port=80, username=None, password=None, num_of_sessions=0):
    if num_of_sessions == 0:
        return

    global tcp_sessions_lst
    print(f'Generate {num_of_sessions} TCP <port {port}> sessions')

    for i in range(num_of_sessions):
        tcp_sessions_lst.append(socket_creation(hostname, port, socket.SOCK_STREAM, username, password))


def create_udp_sessions_lst(hostname: str, port=80, username=None, password=None, num_of_sessions=0):
    if num_of_sessions == 0:
        return

    global tcp_sessions_lst
    print(f'Generate {num_of_sessions} UDP <port {port}> sessions')

    for i in range(num_of_sessions):
        tcp_sessions_lst.append(socket_creation(hostname, port, socket.SOCK_DGRAM, username, password))


def create_http_sessions_lst(hostname: str, username=None, password=None, num_of_sessions=0):
    for i in range(num_of_sessions):
        webbrowser.open_new_tab(f"http://{hostname}")

    #create_tcp_sessions_lst(hostname, 80, username, password, num_of_sessions)


def create_https_sessions_lst(hostname: str, username=None, password=None, num_of_sessions=0):
    for i in range(num_of_sessions):
        webbrowser.open_new_tab(f"https://{hostname}")

    # create_tcp_sessions_lst(hostname, 443, username, password, num_of_sessions)


def close_all():
    global resources_lst
    global is_already_closed
    if is_already_closed:
        return

    is_already_closed = True
    print('Trying to close the connections...')

    for resource_lst in resources_lst:
        if not resource_lst or len(resource_lst) == 0:
            continue

        for res_el in resource_lst:
            if not res_el:
                continue

            try:
                res_el.close()
                print(f'Connection of type {type(res_el)} has closed...')
            except Exception as e:
                print(f'{type(res_el)} hasn\'t closed: {str(e)}')


def gen_bunch_of_sessions(target_ip: str, username=None, password=None, telnet_num=0, ssh_num=0, http_num=0, https_num=0, tftp_num=0):
    threads_lst = []

    telnet_thread = threading.Thread(name='telnet_thread', target=create_telnet_sessions_lst,
                                     args=(target_ip, username, password, telnet_num,))
    threads_lst.append(telnet_thread)

    ssh_thread = threading.Thread(name='ssh_thread', target=create_ssh_sessions_lst,
                                  args=(target_ip, username, password, ssh_num,))
    threads_lst.append(ssh_thread)

    http_thread = threading.Thread(name='http_thread', target=create_http_sessions_lst,
                                   args=(target_ip, username, password, http_num,))
    threads_lst.append(http_thread)

    https_thread = threading.Thread(name='https_thread', target=create_https_sessions_lst,
                                    args=(target_ip, username, password, https_num,))
    threads_lst.append(https_thread)

    tftp_thread = threading.Thread(name='tftp_thread', target=create_udp_sessions_lst,
                                   args=(target_ip, 69, username, password, tftp_num,))
    threads_lst.append(tftp_thread)

    # start all threads
    for thr_el in threads_lst:
        thr_el.start()
    # wait for all threads
    for thr_el in threads_lst:
        thr_el.join()


def run_all(target_ip: str, username=None, password=None, telnet_num=0, ssh_num=0, http_num=0, https_num=0, tftp_num=0):
    global all_session_thread_lst
    num_of_rounds = 5

    for i in range(num_of_rounds):
        wait_sec = random.randint(1, 1)
        time.sleep(wait_sec)
        print(f'round {i}: wait {wait_sec} seconds')
        print('=' * 100)
        sess_th = threading.Thread(name='all_session_thread', target=gen_bunch_of_sessions,
                                   args=(target_ip, username, password, telnet_num, ssh_num, http_num, https_num, tftp_num,))
        sess_th.start()
        all_session_thread_lst.append(sess_th)


if __name__ == '__main__':
    run_all('60.0.0.64', 'marvell', password=None, telnet_num=0, ssh_num=0, http_num=0, https_num=1, tftp_num=0)
    close_all()
