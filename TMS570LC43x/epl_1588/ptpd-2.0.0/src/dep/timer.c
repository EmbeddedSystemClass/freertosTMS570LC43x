/* timer.c */

#include "../ptpd.h"

/* An array to hold the various system timer handles. */
static TimerHandle_t  ptpdTimers[TIMER_ARRAY_SIZE];
static bool ptpdTimersExpired[TIMER_ARRAY_SIZE];
 
static void vTimerCallback(TimerHandle_t xTimer)
{
	configASSERT(xTimer);
	int index = (int)pvTimerGetTimerID(xTimer);
	if(index >= TIMER_ARRAY_SIZE){
		//TODO: you have a problem
	}
	else{
		ptpdTimersExpired[index] = TRUE;
	}
}

void initTimer(void)
{
	int32_t i;

	DBG("initTimer\n");

	/* Create the various timers used in the system. */
  for (i = 0; i < TIMER_ARRAY_SIZE; i++)
  {
		// Mark the timer as not expired.
		// Initialize the timer.
//		sys_timer_new(&ptpdTimers[i], vTimerCallback, osTimerOnce, (void *) i);
		ptpdTimers[i] = xTimerCreate(
				"Timer",
				pdMS_TO_TICKS(1000),
				pdFALSE,
				 (void *)i,
				vTimerCallback
				);
		ptpdTimersExpired[i] = FALSE;

		if(ptpdTimers[i] == NULL){
			//TODO: handle
		}

	}
}

void timerStop(int32_t index)
{
	/* Sanity check the index. */
	if (index >= TIMER_ARRAY_SIZE) return;

	// Cancel the timer and reset the expired flag.
	DBGV("timerStop: stop timer %d\n", index);
	xTimerStop(ptpdTimers[index], 0);
	ptpdTimersExpired[index] = FALSE;
}

void timerStart(int32_t index, uint32_t interval_ms)
{
	/* Sanity check the index. */
	if (index >= TIMER_ARRAY_SIZE) return;

	// Set the timer duration and start the timer.
	DBGV("timerStart: set timer %d to %d\n", index, interval_ms);
	ptpdTimersExpired[index] = FALSE;
	int block_for_ticks = 1;
	interval_ms /= portTICK_PERIOD_MS;
	if(!interval_ms){
		interval_ms = 10;
	}
	if(xTimerChangePeriod(ptpdTimers[index], interval_ms, block_for_ticks) != pdPASS){
		//TODO: handle
	}
}

bool timerExpired(int32_t index)
{
	/* Sanity check the index. */
	if (index >= TIMER_ARRAY_SIZE) return FALSE;

	/* Determine if the timer expired. */
	if (!ptpdTimersExpired[index]) return FALSE;
	ptpdTimersExpired[index] = FALSE;
	return TRUE;
}
