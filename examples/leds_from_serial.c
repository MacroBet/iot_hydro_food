/*
 * Copyright (c) 2006, Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */

#include "contiki.h"
#include <stdio.h>
#include "os/dev/leds.h"
#include "sys/etimer.h"
#include "os/dev/serial-line.h"
#include <string.h>
#include <unistd.h> 

PROCESS(led_blink, "Led blink");
AUTOSTART_PROCESSES(&led_blink);

PROCESS_THREAD(led_blink, ev, data){
	char green[6];
	char red[4];
	char yellow[7];
	strcpy(green, "GREEN");
	strcpy(red, "RED");
	strcpy(yellow, "YELLOW");

	PROCESS_BEGIN();
	while(1){
		PROCESS_WAIT_EVENT_UNTIL(ev == serial_line_event_message);
		if(strcmp(data, green) == 0){
			leds_single_on(LEDS_GREEN);
			sleep(2);
			leds_single_off(LEDS_GREEN);

		}
		else if(strcmp(data, red) == 0){
			leds_set(LEDS_NUM_TO_MASK(LEDS_RED));
		}
		else if(strcmp(data, yellow) == 0){
			leds_on(LEDS_NUM_TO_MASK(LEDS_YELLOW));
		}
	}
	PROCESS_END();
}
