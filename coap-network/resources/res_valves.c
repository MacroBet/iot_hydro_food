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
#include "coap-engine.h"
#include "sys/node-id.h"
#include "../app_var.h"

static void res_get_handler(coap_message_t *request, coap_message_t *response, uint8_t *buffer, uint16_t preferred_size, int32_t *offset);
static void res_event_handler(void);
// 
static int mode = 0;
/*
 * A handler function named [resource name]_handler must be implemented for each RESOURCE.
 * A buffer for the response payload is provided through the buffer pointer. Simple resources can ignore
 * preferred_size and offset, but must respect the REST_MAX_CHUNK_SIZE limit for the buffer.
 * If a smaller block size is requested for CoAP, the REST framework automatically splits the data.
 */
EVENT_RESOURCE(res_obs,
         "title=\"valve status\";rt=\"Text\";obs",
         res_get_handler,
         res_post_handler,
         NULL,
         NULL, 
		 res_event_handler);

// valve 
// 0 -> closed
// 1 -> irrigator open
// 2 -> valve open

static void res_event_handler(void){

  coap_notify_observers(&res_obs);
}


static void res_get_handler(coap_message_t *request, coap_message_t *response, uint8_t *buffer, uint16_t preferred_size, int32_t *offset) {
  
  char message[64];
  int length = 64;
  snprintf(message, length, "{\"node\": %d, \"valve_status\": %d}", node_id, valve_status );

  size_t len = strlen(message);
  memcpy(buffer, (const void *) message, len);

  coap_set_header_content_format(response, TEXT_PLAIN);
  coap_set_header_etag(response, (uint8_t *)&len, 1);
  coap_set_payload(response, buffer, len);
}

static void res_post_handler(coap_message_t *request, coap_message_t *response, uint8_t *buffer, uint16_t preferred_size, int32_t *offset) {

 if(request != NULL)
        LOG_INFO("Post request received");

  size_t len = 0;
  const char *mode = NULL;

  len = coap_get_post_variable(request, "mode", &mode);
  if(len > 0 && strcmp(mode, "1") == 0) {
        
        if(valve_status == 0 ) {
            valve_status = 1;
            LOG_INFO("Start watering");

        } else if(valve_status == 1) {
            
            LOG_INFO("Watering already started");

        } if(valve_status == 2) {
            char const *const message = "Impossible to start watering";
            size_t len = strlen(message); 
            // Copy the response in the transmission buffer
            memcpy(buffer, message, length);

            // Prepare the response
            coap_set_header_content_format(response, TEXT_PLAIN); 
            coap_set_header_etag(response, (uint8_t *)&length, 1);
            coap_set_payload(response, buffer, length);
                      
            LOG_INFO("Impossible to start watering");
        
        } else
            coap_set_status_code(response, BAD_REQUEST_4_00);

  } else if(len > 0 && strcmp(mode, "2") == 0){
       
       if(valve_status == 0 ) {
            valve_status = 2;
            LOG_INFO("Start charging");

        } else if(valve_status == 2) {
            
            LOG_INFO("Charging already started");

        } if(valve_status == 1) {
            
             char const *const message = "Impossible to start charging";
            size_t len = strlen(message); 
            memcpy(buffer, message, length);

            coap_set_header_content_format(response, TEXT_PLAIN); 
            coap_set_header_etag(response, (uint8_t *)&length, 1);
            coap_set_payload(response, buffer, length);
                      
            LOG_INFO("Impossible to start charging");
        
        } else
            coap_set_status_code(response, BAD_REQUEST_4_00);

    else if(len > 0 && strcmp(mode, "0") == 0){
       
       if(valve_status == 0 ) {
            LOG_INFO("Valves closed");

        } else if(valve_status == 2) {
            valve_status = 0
            LOG_INFO("Valves closed");

        } if(valve_status == 1) {
            valve_status = 0
            LOG_INFO("Valves closed");
        
        } else
            coap_set_status_code(response, BAD_REQUEST_4_00);
    }

}






// unsigned int accept = -1;
//   coap_get_header_accept(request, &accept);
//   if(accept == -1 || accept == APPLICATION_JSON) {
//     content_len = 0;
//     CONTENT_PRINTF("{\"DR1175\":[");
//     CONTENT_PRINTF("{\"Humidity\":\"%d\"},", ht_sensor.value(HT_SENSOR_HUM));
//     CONTENT_PRINTF("{\"Light\":\"%d\"},", light_sensor.value(0));
//     CONTENT_PRINTF("{\"Temp\":\"%d\"}", ht_sensor.value(HT_SENSOR_TEMP));
//     CONTENT_PRINTF("]}");
//     coap_set_header_content_format(response, APPLICATION_JSON);
//     coap_set_payload(response, (uint8_t *)content, content_len);
//   }