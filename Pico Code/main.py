from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
import time
import network
import urequests
import ujson

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
display = SSD1306_I2C(128, 64, i2c)

joy_x = ADC(Pin(27))
joy_y = ADC(Pin(26))
toggleButton = Pin(0, Pin.IN, Pin.PULL_UP)
sendButton = Pin(1, Pin.IN, Pin.PULL_UP)

WIFI_SSID = 'YOUR_SSID'
WIFI_PASSWORD = 'YOUR_PASSWORD'

SUPABASE_URL = "https://noxkxkyazozdqslfieir.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5veGt4a3lhem96ZHFzbGZpZWlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI5MDA0NjAsImV4cCI6MjA1ODQ3NjQ2MH0.2XhaTevNpeaGd7Bh8C598jUeWpn2f32oZ1HHSp3__9s"
select_url = f"{SUPABASE_URL}/rest/v1/Messages?select=*&order=sent_at.desc"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    # "Content-Type": "application/json",
}

message_storage = []

screen = True
last_toggle = 0

cursor = 0

trigger = True
iterations = 0

line_height = 8
spacing = 2

sent = False
ascii_character = ''
message_str = ''

keypad_columns = [6,7,8,9]
keypad_rows = [2,3,4,5]

col_pins = []
row_pins = []

matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'B'],
               ['7', '8', '9', 'C'],
               ['F', '0', 'E', 'D']]

for x in range(0,4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)
    
def scankeys():
    global message_str, ascii_character
    for row in range(4):
        for col in range(4):
            row_pins[row].high()
            key = None
            
            if col_pins[col].value() == 1:
                if len(ascii_character) < 2:
                    ascii_character += matrix_keys[row][col]
                if len(ascii_character) == 2:
                    if ascii_character == '7F':
                        message_str = message_str[:-1]
                    elif ascii_character == '1B':
                        message_str = ''
                    else:
                        message_str += chr(int(ascii_character, 16))
                    ascii_character = ''
                time.sleep(0.3)
                    
        row_pins[row].low()
        
def anykey():
    for row in range(4):
        row_pins[row].high()
        for col in range(4):
            if col_pins[col].value() == 1:
                return True  
        row_pins[row].low()  
    return False

def connect(SSID, PASS):
    printText('Connecting...')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASS)

    while not wlan.isconnected():
        time.sleep(1)
        
    printText('Connected!')
    return

def split_into_lines(string, limit=16):
    words = string.split(" ")
    lines = []
    current_line = ''

    for word in words:
        if len(current_line) == 0:
            current_line += word
        elif len(f"{current_line} {word}" ) <= limit:
            current_line = current_line + ' ' + word
        else:
            lines.append(current_line)
            current_line = word
            
    if current_line:
        lines.append(current_line)

    return lines

def parse_timestamp(timestamp):
    date_time_str = timestamp.rstrip('Z')
    date_str, time_str = date_time_str.split('T')
    year, month, day = map(int, date_str.split('-'))
    month_name = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"][month - 1]
    formatted_date = f"{month_name} {day}, {year}"
    time_parts = time_str.split(':')
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    formatted_time = f"{hour:02}:{minute:02}"
    return formatted_date, formatted_time

def getMessages(url, headers):
    ms = []
    response = urequests.get(url=url, headers=headers)

    for message in ujson.loads(response.text):
        _, time = parse_timestamp(message['sent_at'])
        ms.append(f"{time} {message['sender']}: {message['content']}")
    
    return ms

def formatMessages(messages):
    rows = []
    for message in messages:
        lines = split_into_lines(message)
        rows += lines
        rows.append(' ')
    return rows

def displayMessages(formatted_messages):
    display.fill(0)
    for i in range(cursor, min(cursor + 6, len(formatted_messages))):
        display.text(formatted_messages[i], 0, (i - cursor) * (line_height + spacing))
    display.show()

def joystick(max_len):
    global cursor, message_storage
    y_val = joy_y.read_u16()
    if y_val > 60000 and cursor > 0:
        cursor -= 1
        time.sleep(0.15)
    elif y_val < 30000 and cursor < max_len:
        cursor += 1
        time.sleep(0.15)
        
def printASCIIMessage(ASCII, mess):
    display.fill(0)
    display.text(f"ASCII: {ASCII}", 0, 0)
    
    message = split_into_lines(mess)
    
    for i, m in enumerate(message):
        display.text(m, 0, (i + 1) * (line_height + spacing))
    display.show()

def printText(string, x=0, y=0):
    display.fill(0)
    display.text(str(string), int(x), int(y))
    display.show()
    
def sendMessage(message):
    global SUPABASE_URL, headers
    sendUrl = f"{SUPABASE_URL}/rest/v1/Messages"
    data = {
        'content': str(message),
        'sender': "Whatney",
        'recipient': "JPL"
    }
    response = urequests.post(url=sendUrl, json=data, headers=headers)
    if response.status_code in [200, 201]:
        return True
    else:
        print(f"Error {response.status_code}: {response.text}")
        return False
    
def toggle_callback(pin):
    global screen, last_toggle
    now = time.ticks_ms()
    if time.ticks_diff(now, last_toggle) > 200:
        screen = not screen
        print("Screen toggled:", screen)
        last_toggle = now
    
toggleButton.irq(trigger=Pin.IRQ_RISING, handler=toggle_callback)

def main():
    global screen, trigger, iterations, message_storage, message_str
    
    try:
        connect(WIFI_SSID, WIFI_PASSWORD)
        time.sleep(0.5)
        while True:
            if screen:
                if trigger or iterations > 20:
                    message_storage = formatMessages(getMessages(select_url, headers))
                    trigger = False
                    iterations = 0
                joystick(len(message_storage) - 6)
                displayMessages(message_storage)
                iterations += 1
            else:
                display.fill(0)
                printASCIIMessage(ascii_character, message_str)
                if not sendButton.value():
                    display.fill(0)
                    display.text('Confirm send?', 0, 0)
                    display.text("press 'send'", 0, 20)
                    display.text('or cancel by', 0, 30)
                    display.text('pressing any', 0, 40)
                    display.text('other key', 0, 50)
                    display.show()
                    time.sleep(0.2)
                    send = False
                    cancel = False
                    while True:
                        if not sendButton.value():
                            send = True
                            cancel = False
                            break
                        if anykey():
                            cancel = True
                            send = False
                            break
                    display.fill(0)
                    display.show()
                    if send:
                        printText('Sending...')
                        status = sendMessage(message_str)
                        if status:
                            printText('Sent!')
                            message_str = ''
                            time.sleep(2)
                        else:
                            printText('Send Failed!')
                            time.sleep(1)
                scankeys()
    finally:
        display.fill(0)
        display.show()

if __name__ == '__main__':
    main()
