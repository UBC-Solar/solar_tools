# <span style="color:orange">Hardware Verification Guide</span> 🌞  

## Manual Process:
1) Check for pin to end-point connection: Using a multimeter to probe the STM32 Pins to the endpoint of that pad connection to either a header, component, or connector through holes. One tip of the probe would be placed at the STM32 Pin and the other probe would be placed at the desired end. For the CAN_TX and CAN_RX, the continuity of those pins would be checked with its respective CAN transceivers. In addition, check the shorts for the pin connected to the Debug LED that will be used to confirm a CAN message is received.
   
2) Check for Pin shorts for non-GPIO pins: Since pins such as VDD and GND as they cannot have the values read, a multimeter will be used to probe that pin and its neighboring pins. As shown on the figure, a continuity test will be conducted for all non-GPIO pins to non-GPIO pins.
   
3) Check for shorts between the boot pins. As the boot pins cannot be read as well through the STM, a multimeter will be used to check shorts between the boot and its neighboring pins.

## Software Process:
1) Connect the ST-link (make sure to include the 5V to the PCB) as well as the PCAN connector to the PCB under testing. After, configure the pins to match the logic such as changing the pins for CAN_TX, CAN_RX, Debug pins, etc. After all the pins are set correctly, run the code and look at PCAN view.
2) Under PCAN view, there will be different values on the receive section. Convert the databytes to decimals and with the first data entry representing the port letter (52 = A, 53 = B, 54 = C, 55 = D) and the pin number following after (e.g 001,002). The CAN-ID represents whether the short is between a VCC (580h) between GND (581h) and between GPIOs (582h).
3) To confirm that the STM32 can receive CAN messages, transmit through PCAN view with a CAN-ID of 0x103 and see if the debug LED lights up!

## Debug Errors:
- Make sure that the appropriate power sources are connected including 3.3V **and 5V**.
- Always set the debug LED as a GPIO output and work around that pin for GPIO input/output initializations. 
- Make sure when transmitting data to the STM32, it matches the CAN-ID mentioned above.


