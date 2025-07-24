# A two-way communication system with Raspberry Pi Pico W

### Preview:
![IMG_4340 2](https://github.com/user-attachments/assets/27e0824d-c399-4e26-93c6-02bd138860f6)



### Description
This project is a two-way communication system built with a Supabase backend. On one side, a React web app allows users to send messages from a computer. On the other side, a Raspberry Pi Pico with Wi-Fi connects to the backend to both send and receive messages.

Inspired by The Martian by Andy Weir, the hardware setup includes a keypad for typing messages in hexadecimal ASCII format. These messages are sent to the Supabase backend. The Pico then fetches incoming messages and displays them on an OLED screen. A joystick allows the user to scroll through the messages on the display.


## Hardware Setup

### Required Components
- Raspberry Pi Pico W
- SSD1306 OLED
- Keypad
- Joystick Module 
- Limit Switches or Buttons (x2) 
- Jumper Wires


### Connections

**Display:**
| SSD1306  | Raspberry Pi Pico W |
|----------|----------|
| GND    | GND     |
| VCC    | 3V3  |
| SCL    | GP17  |
| SDA    | GP16  |

**Joystick:**
| Joystick Module  | Raspberry Pi Pico W |
|----------|----------|
| GND    | GND     |
| +5V    | 3V3  |
| VRx    | GP26 |
| VRy    | GP27  |

**Switch/Button:**
| Limit Switch 1  | Raspberry Pi Pico W |
|----------|----------|
| GND    | GND     |
| VCC    | 3V3  |
| Data    | GP0  |

**Switch/Button:**
| Limit Switch 2  | Raspberry Pi Pico W |
|----------|----------|
| GND    | GND     |
| VCC    | 3V3  |
| Data    | GP1  |

**Keypad:**
| Keypad  | Raspberry Pi Pico W |
|----------|----------|
| 1    | GP9     |
| 2    | GP8  |
| 3    | GP7  |
| 4    | GP6  |
| 5    | GP5  |
| 6    | GP4  |
| 7    | GP3  |
| 8    | GP2  |

## Backend (Supabase)

The project uses supabase as a backend to store and retrieve messages. You will need to create a table named `Messages` and add the following columns:

| column_name | data_type                |
| ----------- | ------------------------ |
| id          | bigint                   |
| content     | text                     |
| sent_at     | timestamp with time zone |
| read        | boolean                  |
| sender      | text                     |
| recipient   | text                     |

Make sure to use the right credentials in the project files.

## Running the Web App

1. Clone the repository
2. Go to the `Frontend Web App` folder using `cd 'Frontend Web App'`
3. Create a `.env` file and create paste in your supabase url and key with the names `VITE_SUPABASE_URL` and `VITE_SUPABASE_KEY`
4. Run `npm install` to install the dependencies
5. Start the development server with `npm run dev`

### NB! Create a user on the supabase `Authentication` page. 

You should now see a login page. Once you log in with your credentials you will see the messages. Refresh to see new messages sent from the Raspberry Pi device.

# References
`ssd1306.py` by @Guitarman9119 on Github https://github.com/Guitarman9119/Raspberry-Pi-Pico-/tree/main/SSD1306%20OLED%20Display

