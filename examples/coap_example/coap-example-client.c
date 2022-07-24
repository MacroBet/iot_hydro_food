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
#include "contiki-net.h"
#include "coap-engine.h"
#include "coap-blocking-api.h"

/* Log configuration */
#include "app_var.h"
#include "coap-log.h"
#define LOG_MODULE "App"
#define LOG_LEVEL  LOG_LEVEL_APP

#define SERVER_EP "coap://[fd00::1]:5683"

static struct etimer periodic_timer;
bool registered = false;
static int period = 0;

void client_chunk_handler(coap_message_t *response)
{
	const uint8_t *chunk;

	if(response == NULL) {
		LOG_INFO("Request timed out");
		return;
	}
	registered = true;
	int len = coap_get_payload(response, &chunk);
	LOG_INFO("|%.*s \n", len, (char *)chunk);
}

PROCESS(node, "node");
AUTOSTART_PROCESSES(&node);

int counter = 0;

extern coap_resource_t res_obs;

PROCESS_THREAD(node, ev, data)
{
  srand(time(NULL));
  static coap_endpoint_t my_server;
  static coap_message_t request[1];


  PROCESS_BEGIN();

  PROCESS_PAUSE();

  LOG_INFO("Starting sensor node\n");

  coap_activate_resource(&res_obs, "obs");

  coap_endpoint_parse(SERVER, strlen(SERVER), &my_server);

  coap_init_message(request, COAP_TYPE_CON, COAP_GET, 0);  
  coap_set_header_uri_path(request, "registry");
  COAP_BLOCKING_REQUEST(&my_server, request, client_chunk_handler);
  printf("--Registred--\n");

  while(!registered){
    LOG_DBG("Retrying with server\n");
    COAP_BLOCKING_REQUEST(&my_server, request, client_chunk_handler);
  }

  etimer_set(&periodic_timer, 30*CLOCK_SECOND);
  
  while(1) {
    PROCESS_WAIT_EVENT();

      if (ev == PROCESS_EVENT_TIMER && data == &periodic_timer){
	  counter++;
	  res_obs.trigger();
	  period++;
	  etimer_reset(&periodic_timer);
      }
    }

  PROCESS_END();
}