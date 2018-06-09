import rabird.winio
import time
import atexit
import sys
import string

# KeyBoard Commands
# Command port
KBC_KEY_CMD = 0x64
# Data port
KBC_KEY_DATA = 0x60

__winio = None

shift_character = r'!@#$%^&*()_+{}|:"<>?~'

WordDict = {'a': '1e', 'b': '30', 'c': '2e', 'd': '20', 'e': '12', 'f': '21', 
            'g': '22', 'h': '23', 'i': '17', 'j': '24', 'k': '25', 'l': '26', 
            'm': '32', 'n': '31', 'o': '18', 'p': '19', 'q': '10', 'r': '13', 
            's': '1f', 't': '14', 'u': '16', 'v': '2f', 'w': '11', 'x': '2d', 
            'y': '15', 'z': '2c', '0': '0b', '1': '02', '2': '03', '3': '04',
            '4': '05', '5': '06', '6': '07', '7': '08', '8': '09', '9': '0a',
            '!': '02', '"': '28', '#': '04', '$': '05', '%': '06', '&': '08', 
            '\'':'28', '(': '0a', ')': '0b', '*': '09', '+': '0d', ',': '33',
            '-': '0c', '.': '34', '/': '35', ':': '27', ';': '27', '<': '33',
            '=': '0d', '>': '34', '?': '35', '@': '03', '[': '1a', '\\': '2b',
            ']': '1b', '^': '07', '_': '0c', '`': '29', '{': '1a', '|': '2b',
            '}': '1b', '~': '29'}

def __get_winio():
    global __winio

    if __winio is None:
            __winio = rabird.winio.WinIO()
            def __clear_winio():
                    global __winio
                    __winio = None
            atexit.register(__clear_winio)

    return __winio

def wait_for_buffer_empty():
    '''
    Wait keyboard buffer empty
    '''

    winio = __get_winio()

    dwRegVal = 0x02
    while (dwRegVal & 0x02):
            dwRegVal = winio.get_port_byte(KBC_KEY_CMD)

def key_down(scancode):
    winio = __get_winio()

    wait_for_buffer_empty();
    winio.set_port_byte(KBC_KEY_CMD, 0xd2);
    wait_for_buffer_empty();
    winio.set_port_byte(KBC_KEY_DATA, scancode)

def key_up(scancode):
    winio = __get_winio()

    wait_for_buffer_empty();
    winio.set_port_byte( KBC_KEY_CMD, 0xd2);
    wait_for_buffer_empty();
    winio.set_port_byte( KBC_KEY_DATA, scancode | 0x80);

def key_press(scancode, press_time = 0.2):
    key_down( scancode )
    time.sleep( press_time )
    key_up( scancode )

def str_to_hex(str):
    return int(str, 16)

def out_put_password(password, interval):
    for c in password:
        if (c in string.ascii_uppercase) or (c in shift_character):
            key_down(0x2a)
            key_press(str_to_hex("0x" + WordDict.get(c.lower())), press_time=interval/1000)
            key_up(0x2a)
        else:
            key_press(str_to_hex("0x" + WordDict.get(c)), press_time=interval/1000)
        
def main(args):
    password, interval = (args[1], int(args[2]))
    # password = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    out_put_password(password, interval)


# Press 'A' key
# Scancodes references : https://www.win.tue.nl/~aeb/linux/kbd/scancodes-1.html
if __name__ == '__main__':
    main(sys.argv)
    # key_press(0x1E)