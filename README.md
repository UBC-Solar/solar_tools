# <span style="color:orange">Hardware Verification Guide</span> 🌞  

## Manual Process:
1) Check for pin to end-point connection: Using a multimeter to probe the STM32 Pins (VCC and GND) to the endpoint of that pad connection to either a header, component, or connector through holes. One tip of the probe would be placed at the STM32 Pin and the other probe would be placed at the desired end. For the CAN_TX and CAN_RX, the continuity of those pins would be checked with its respective CAN transceivers. In addition, check the shorts for the pin connected to the Debug LED that will be used to confirm a CAN message is received.
   
2) Check for Pin shorts for non-GPIO pins: Since pins such as VDD and GND as they cannot have the values read, a multimeter will be used to probe that pin and its neighboring pins. In addition, the GPIO pins configured as debug pins or oscillatory pins must also be checked through a continuity test with a multimeter.
   
3) Check for shorts between the boot pins. As the boot pins cannot be read as well through the STM32, a multimeter will be used to check shorts between the boot and its neighboring pins.

## Software Process:
1) Connect the ST-link (make sure to include the 5V to the PCB) as well as the PCAN connector to the PCB under testing. After, configure the pins to match the logic such as changing the pins for CAN_TX, CAN_RX, Debug pins, etc. After all the pins are set correctly, run the code and look at PCAN view.
   
2) Under PCAN view, there will be different values on the receive section. Convert the databytes to decimals and with the first data entry representing the port letter (52 = A, 53 = B, 54 = C, 55 = D) and the pin number following after (e.g 001,002). The CAN-ID represents whether the short is between a VCC (580h) between GND (581h) and between GPIOs (582h). Once you receive this value, bring out a multimeter to probe that pin manually to find the short and rework the STM32 accordingly. After a short is detected, there will be a 2.5 second delay until the code continues again to detect another short.
   
3) To confirm that the STM32 can receive CAN messages, transmit through PCAN view with a CAN-ID of 0x103, (0x104, 0x105, 0x106 works as well) and see if the debug LED lights up!
   
4) Repeat the Software Check after reworking the STM32 to remove the following shorts until nothing shows under PCAN view!

## Debug Tips:
- Make sure that the appropriate power sources are connected including 3.3V **and 5V**.
- Always set the debug LED as a GPIO output and set the neighbouring pins to input pins. If the pin alignment does not match up (For example, the neighbouring pin also needs to be GPIO_output), then use a multimeter to probe those pins manually to prevent accidental shorts.
- Make sure when transmitting data to the STM32, it matches the CAN-ID mentioned above.
- If a pin is appearing to be shorted on PCAN view, but a multimeter check was done and proven that it wasn't shorted, check if that pin is connected through an **external** pull-up/down resistor that can affect the reading. For example, an internal pull-down resistor was connected with an external pull-up resistor, this will create a voltage divider circuit the pin to only read the value of the internal pull-down resistor. (~2.2V).

**Pictures:**

PCAN View
<img width="1918" height="999" alt="image" src="https://github.com/user-attachments/assets/c8d1c3c3-3986-47ad-82fd-ba205d4b9550" /> 

ST-Link connected to PCB

<img width="688" height="913" alt="image" src="https://github.com/user-attachments/assets/96264082-c290-4755-94ee-cdf01c5f30b6" />

Peak Connector to PCB

<img width="776" height="1019" alt="image" src="https://github.com/user-attachments/assets/233af3b7-d533-41aa-a3bc-c349c8df3020" />


**Limitations:**

The following hardware verification process only checks for the STM32 being properly connected to the pads, shorts between the STM32 pins, and the ability to receive/transmit CAN signals through the transceiver. Therefore, UART, I2C, SPI communication was not directly tested, but was under the assumption that if the GPIO pins were connected, the communication systems would work as well. In addition, **the VCC and GND pins are not directly tested to be shorted to non-neighbouring pins** due to the small possibility of it occuring during the reflow soldering process.

This verificiation steps does not check for faults within the circuitry and PCB design (For example, this code will not check the routes between components that are not connected to the STM32). **This process is mainly a sanity check to ensure that the STM32 is connected to the board properly** as the main issues typically arise within the microcontroller itself. 
