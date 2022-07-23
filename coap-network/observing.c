/*
 * Copyright (c) 2020, Carlo Vallati, University of Pisa
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
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "contiki.h"
#include "coap-engine.h"
#include "sys/etimer.h"
#include "app_var.h"
#include "dev/button-hal.h"
/* Log configuration */
#include "sys/log.h"

#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_APP
/*
 * Resources to be activated need to be imported through the extern keyword.
 * The build system automatically compiles the resources in the corresponding sub-directory.
 */
extern coap_resource_t  res_valves; 
int valve_status = 0;
int charge = 0;
static struct stimer timer_charge;

PROCESS(er_example_server, "Status valve server");
AUTOSTART_PROCESSES(&status_valve_server);

PROCESS_THREAD(status_valve_server, ev, data)
{
  button_hal_button_t *btn;

  PROCESS_BEGIN();
  
  btn = button_hal_get_by_index(0);
  
  PROCESS_PAUSE();

  LOG_INFO("Starting Status valves Server\n");

  coap_activate_resource(&res_valves, "obs");
  
  while(1) {
    
    if(charge == 1 && stimer_exipred(&timer_charge)) {
      valve_status = 0;
      res_valves.trigger();
    }
    PROCESS_YIELD();

    if(ev == button_hal_press_event && valve_status != 1 ) {
      btn = (button_hal_button_t *)data;
      LOG_INFO("Press event (%s)\n", BUTTON_HAL_GET_DESCRIPTION(btn));

      if(btn == button_hal_get_by_id(BUTTON_HAL_ID_BUTTON_ZERO)) {
        LOG_INFO("This was button 0, on pin %u\n", btn->pin);
        valve_status = 1;
        res_valves.trigger();
      }
    } else if(ev == button_hal_release_event) {
      btn = (button_hal_button_t *)data;
      LOG_INFO("Release event (%s)\n", BUTTON_HAL_GET_DESCRIPTION(btn));

    } else if(ev == button_hal_periodic_event && valve_status != 2) {

      btn = (button_hal_button_t *)data;
      LOG_INFO("Periodic event, %u seconds (%s)\n", btn->press_duration_seconds,
             BUTTON_HAL_GET_DESCRIPTION(btn));

      if(btn->press_duration_seconds > 2) {
        LOG_INFO("%s pressed for more than 5 secs. Do custom action\n",
               BUTTON_HAL_GET_DESCRIPTION(btn));
        valve_status = 2;
        charge = 1;
        res_valves.trigger();
        stimer_set(&timer_charge, CLOCK_SECOND * 4);
      }
    }
  }                             

  PROCESS_END();
}
