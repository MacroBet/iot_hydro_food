
#include "contiki.h"
#include "net/netstack.h"
#include "os/dev/leds.h"
#include < stdio.h>
#include < string.h>
#include "sys/ctimer.h"

PROCESS(led_blink_process, "led blink process");
AUTOSTART_PROCESSES(&led_blink_process);
static struct ctimer b_leds;

void blink_callback()
{
    if ((leds_get() & LEDS_RED) == 1 && (leds_get() & LEDS_GREEN) == 2)
    {
        leds_toggle(LEDS_GREEN);
        ctimer_set(&b_leds, 1 * CLOCK_SECOND, blink_callback, NULL);
        return;
    }
    if ((leds_get() & LEDS_RED) == 1)
    {
        leds_toggle(LEDS_RED);
        leds_toggle(LEDS_GREEN);
        ctimer_set(&b_leds, 1 * CLOCK_SECOND, blink_callback, NULL);
        return;
    }
    if ((leds_get() & LEDS_GREEN) == 2)
    {
        leds_toggle(LEDS_RED);
        leds_toggle(LEDS_GREEN);
        ctimer_set(&b_leds, 1 * CLOCK_SECOND, blink_callback, NULL);
        return;
    }
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(led_blink_process, ev, data)
{
    PROCESS_BEGIN();
    leds_toggle(LEDS_GREEN);
    leds_toggle(LEDS_RED);
    ctimer_set(&b_leds, 5 * CLOCK_SECOND, blink_callback, NULL);
    PROCESS_YIELD();
    PROCESS_END();
}