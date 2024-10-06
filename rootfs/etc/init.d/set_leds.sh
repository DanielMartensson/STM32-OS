#!/bin/bash

# Blue led at STM32-Computer
echo timer > /sys/class/leds/heartbeat/trigger
echo 1 > /sys/class/leds/heartbeat/delay_on
echo 10000 > /sys/class/leds/heartbeat/delay_off
