make TARGET=nrf52840 BOARD=dongle rgb-led-example.dfu-upload PORT=/dev/ttyACM0
make login TARGET=nrf52840 BOARD=dongle PORT=/dev/ttyACM0



make TARGET=nrf52840 BOARD=dongle button-hal-example.dfu-upload PORT=/dev/ttyACM0
make login TARGET=nrf52840 BOARD=dongle PORT=/dev/ttyACM0




make TARGET=nrf52840 BOARD=dongle PORT=/dev/ttyACM0 border-router.dfu-upload
make TARGET=nrf52840 BOARD=dongle PORT=/dev/ttyACM0 connect-router

fd00::f6ce:3609:93f6:201e
sudo apt-get install libcoap-1-0-bin


coap-client -m get coap://[fd00::201:1:1:1]/test/hello
coap-client -m get coap://[fd00::f6ce:3609:93f6:201e]/test/hello

make login TARGET=nrf52840 BOARD=dongle PORT=/dev/ttyACM0


ls -l /dev/serial/by-id
