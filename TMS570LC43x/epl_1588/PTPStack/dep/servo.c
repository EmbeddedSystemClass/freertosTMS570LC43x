/* servo.c */
/*****************************************************************************
COPYRIGHT NOTICE

PTP Notice for PTPd Software

The following copyright notice applies to all files which compose the original
PTPd Software. This notice applies as if the text was explicitly included each
file.

Copyright (c) 2006 Aidan Williams
Copyright (c) 2005-2007 Kendall Correll

Permission is hereby granted to use, copy, modify, and distribute this software
for any purpose and without fee, provided that this notice appears in all
copies. The authors make no representations about the suitability of this
software for any purpose. This software is provided "as is" without express or
implied warranty.

National Semiconductor Notice for Modified Software

The following copyright notice applies Modifications of the PTPd Software 
developed by National Semiconductor Corporation, and distributed by 
National Semiconductor as a Modified Version of the PTPd Software.  

Copyright (c) 2008 National Semiconductor

The associated Modified Software is distributed by National Semiconductor under 
the above PTPd Notice and Permission, and under the following License, 
Restrictions, Disclaimers and Limitations:

LICENSE:  Permission is granted to copy, use, modify and/or distribute the 
Software in Source and/or Binary form, including as an FPGA or other hardware 
implementation of the Software, subject to the Restrictions, Disclaimers and 
Limitations.  NSC and/or its licensors retain ownership of all copyright, 
patent and other intellectual property rights in the Software, and COMPANY 
shall not remove or alter any copyright or other notices associated with the 
Software

RESTRICTIONS: The Software may be distributed only in connection the 
distribution of COMPANY�s Products, and only subject to the following 
additional Restrictions:  (a) NSC Components:  The Software may be used 
only in connection with Components that are incorporated into COMPANY's 
Products; (b) Sublicensing Source:  The Software may be sublicensed in 
Source form, without any right to grant further downstream sublicenses, 
solely in accordance with this Agreement including these Restrictions;  
(c) Confidentiality.  The Source form of the Software is confidential, 
and unauthorized use or disclosure is prohibited; and (d) Export Compliance.  
The Software is subject to United States export control laws and regulations, 
and any product, software or technical data acquired from NSC, or any direct 
product thereof, shall not be, directly or indirectly, exported, re-exported, 
or released to any destination without first obtaining any export license or 
other approval required by the U.S. government, or other applicable non-U.S. 
governments.  This provision shall survive any termination of this Agreement.

DISCLAIMERS:   The Software is provided "AS IS" without warranty of any kind, 
including any warranty as to the design or manufacture of COMPANY Products 
incorporating Components.  NSC and its licensors expressly disclaim all 
warranties, expressed, implied or otherwise, including without limitation, 
warranties of merchantability, fitness for a particular purpose and 
non-infringement of intellectual property rights.  
Any COMPANY Product incorporating any Software (or any FPGA or other hardware 
implementation) and associated Components should not be released to production 
without full test, verification, and qualification, including verification of 
the selection, configuration and performance of any Software (or any FPGA or 
other hardware implementation) and/or Components, and including verification 
that the product design meets functional, performance, reliability and any 
applicable export or other regulatory requirements.

LIMITATIONS ON LIABILITY.  NSC or its licensors shall not be liable for any 
direct or indirect or punitive damages of any kind, including but not limited 
to any special, consequential or incidental damages, including any costs of 
labor, delay, requalification, or replacement, and any lost business 
opportunity, profits, or goodwill, whether arising out of the use or 
inability to use the Software (or the use or inability to use any COMPANY 
Product incorporating the Software), even if NSC is advised of the 
possibility of such damages.  In no event shall NSC's aggregate liability from 
any obligation arising out of or in connection with the license or use of the 
Software, under any theory of liability including but not limited to contract, 
tort or promissory fraud, exceed the consideration received by NSC, if any, 
for the license to the Software.  The foregoing limitation shall not apply to 
damages resulting directly from NSC's willful and wanton conduct.  To the 
maximum extent permitted under law, the limitations in this paragraph shall 
apply even if this limited remedy is found to have failed of its essential 
purpose.

******************************************************************************/


#include "../ptpd.h"

// Local prototypes
void PTPUpdateStatus(
    NS_UINT8 stsType,
    RunTimeOpts *rtOpts,
    PtpClock *ptpClock);


void initClock(RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
    DBG( "initClock()\n");
    
    /* clear vars */
    ptpClock->master_to_slave_delay.seconds = ptpClock->master_to_slave_delay.nanoseconds = 0;
    ptpClock->slave_to_master_delay.seconds = ptpClock->slave_to_master_delay.nanoseconds = 0;
    ptpClock->one_way_delay.seconds = ptpClock->one_way_delay.nanoseconds = 0;
    
    ptpClock->observed_variance = 0;
    ptpClock->observed_drift = 0;  /* clears clock servo accumulator (the I term) */
    ptpClock->owd_filt.s_exp = 0;  /* clears one-way delay filter */
    ptpClock->halfEpoch = ptpClock->halfEpoch || rtOpts->halfEpoch;
    rtOpts->halfEpoch = 0;

    /* level clock */
    if(!rtOpts->noAdjust)
        adjFreq(0);

    ptpClock->numSyncsSeen = 0;
    ptpClock->oneWayWriteIdx = 0;
    ptpClock->numOneWayValues = 0;
    ptpClock->rateSampleRateIdx = 0;
    ptpClock->numRateHistValues = 0;
    ptpClock->avgRatesWriteIdx = 0;
    ptpClock->numAvgRatesHistValues = 0;
    ptpClock->currRate = 0;
    ptpClock->didStepFlag = FALSE;

    ptpClock->lastRateAdj = 0;
    ptpClock->ignoreNextRateFlag = FALSE;
    ptpClock->waitingForAdjFlag = FALSE;
    ptpClock->ignoreSyncCount = 8;
    ptpClock->numGoodOffsets = 0;
    
    PTPClockSetRateAdjustment( rtOpts->eplPortHandle, 0, FALSE, FALSE);     // Clear normal rate count
    PTPClockSetRateAdjustment( rtOpts->eplPortHandle, 0, TRUE, FALSE);      // Clear any active temp rate
    PTPSetTempRateDurationConfig( rtOpts->eplPortHandle, (rtOpts->tempRateLength * 1000) / 8);
    
    // Clear the rx queue of any backed up sync msgs
    //TODO: implement
//    MACFlushReceiveFifos( rtOpts->eplPortHandle);
}


void updateDelay(TimeInternal *send_time, TimeInternal *recv_time,
  one_way_delay_filter *owd_filt, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
int x;

    /* calc 'slave_to_master_delay' */
    subTime(&ptpClock->slave_to_master_delay, recv_time, send_time);

    /* update 'one_way_delay' */
    addTime(&ptpClock->one_way_delay, &ptpClock->master_to_slave_delay, &ptpClock->slave_to_master_delay);
    ptpClock->one_way_delay.seconds /= 2;
    ptpClock->one_way_delay.nanoseconds /= 2;
    
    DBG( "One way delay %d, tx send %ds %dns, rx %ds %dns\n", ptpClock->one_way_delay.nanoseconds,
           send_time->seconds, send_time->nanoseconds,
           recv_time->seconds, recv_time->nanoseconds);

    // Keep a history of the last measured one way delays
    if ( ptpClock->numSyncsSeen < 9)
    {
        // Don't average initial one way delays they have too much error in them 
        // and cause spikes in err off later on.
        ptpClock->oneWayAvg.seconds = ptpClock->one_way_delay.seconds;
        ptpClock->oneWayAvg.nanoseconds = ptpClock->one_way_delay.nanoseconds;
        normalizeTime( &ptpClock->oneWayAvg);
    }
    else
    {
        ptpClock->oneWayList[ptpClock->oneWayWriteIdx] = ptpClock->one_way_delay;
        ptpClock->oneWayWriteIdx += 1;
        if ( ptpClock->oneWayWriteIdx >= rtOpts->numOneWayAvgSamples)
            ptpClock->oneWayWriteIdx = 0;
        
        ptpClock->numOneWayValues += 1;
        if ( ptpClock->numOneWayValues > rtOpts->numOneWayAvgSamples)
            ptpClock->numOneWayValues = rtOpts->numOneWayAvgSamples;

        // Avg the one way delays
        ptpClock->oneWayAvg.seconds = 0;
        ptpClock->oneWayAvg.nanoseconds = 0;
        for ( x = 0; x < ptpClock->numOneWayValues; x++)
        {
            addTime( &ptpClock->oneWayAvg, &ptpClock->oneWayAvg, &ptpClock->oneWayList[x]);
        }

        ptpClock->oneWayAvg.seconds /= ptpClock->numOneWayValues;
        ptpClock->oneWayAvg.nanoseconds /= ptpClock->numOneWayValues;
        normalizeTime( &ptpClock->oneWayAvg);
    }

    DBG( "updateDelay:\n\tavg one way:\t\t%ds %dns\n\tone_way_delay:\t\t%ds %dns\n\tmaster_to_slave_delay:\t%ds %dns\n\tslave_to_master_delay:\t%ds %dns\n",
         ptpClock->oneWayAvg.seconds, ptpClock->oneWayAvg.nanoseconds,
         ptpClock->one_way_delay.seconds, ptpClock->one_way_delay.nanoseconds,
         ptpClock->master_to_slave_delay.seconds, ptpClock->master_to_slave_delay.nanoseconds,
         ptpClock->slave_to_master_delay.seconds, ptpClock->slave_to_master_delay.nanoseconds);

    return;
}

Boolean updateOffset(TimeInternal *send_time, TimeInternal *recv_time,
  offset_from_master_filter *ofm_filt, RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
    TimeInternal slvDiff, mstDiff, rateDiff;
    Integer32 limitedOffset;
    Boolean updateFlag;

	//lastSyncSendTimeSec not a member of ptpClock
    //ptpClock->lastSyncSendTimeSec = send_time->seconds;

    /* calc 'master_to_slave_delay' */
    subTime(&ptpClock->master_to_slave_delay, recv_time, send_time);

    /* update 'offset_from_master' */
    subTime(&ptpClock->offset_from_master, &ptpClock->master_to_slave_delay, &ptpClock->oneWayAvg);
    
    DBG( "updateOffset:\n\toffset_from_master:\t%ds %dns\n\tmaster_to_slave_delay:\t%ds %dns\n",
         ptpClock->offset_from_master.seconds, ptpClock->offset_from_master.nanoseconds,
         ptpClock->master_to_slave_delay.seconds, ptpClock->master_to_slave_delay.nanoseconds);

    updateFlag = FALSE;
    
    if ( rtOpts->limiterEnable)
    {
        if ( ptpClock->numGoodOffsets >= 2 && ptpClock->offset_from_master.seconds == 0)
        {
            if ( abs(ptpClock->offset_from_master.nanoseconds) > (int)rtOpts->limiterThresh)
            {
                if ( ptpClock->numGoodOffsets)
                    ptpClock->numGoodOffsets--;

                limitedOffset = (ptpClock->offset_from_master.nanoseconds * (int)rtOpts->limiterLimitMultiplier)/100;

                DBG( "LIMITER: Orig %d, Limited %d\n", ptpClock->offset_from_master.nanoseconds, limitedOffset);
                ptpClock->offset_from_master.nanoseconds = limitedOffset;
                updateFlag = TRUE;
                
                if ( abs(ptpClock->offset_from_master.nanoseconds) > (int)rtOpts->limiterThreshMax)
                {
                    DBG( "LIMITER: Discarding offset %d\n", ptpClock->offset_from_master.nanoseconds);
                    return FALSE;
                }
            }
        }
    
        if ( !updateFlag && ptpClock->offset_from_master.seconds == 0 && 
             abs(ptpClock->offset_from_master.nanoseconds) <= (int)rtOpts->limiterGoodThresh)
        {
            if ( ptpClock->numGoodOffsets < 20)
                ptpClock->numGoodOffsets += 5;
        }
    }
    
    // Determine an instantaneous rate adjust based on differences in master / slave clock 
    // frequencies.
    if ( ptpClock->numSyncsSeen > 1)
    {
        subTime( &slvDiff, recv_time, &ptpClock->prevSyncRxTime);
        subTime( &mstDiff, send_time, &ptpClock->prevSyncTxTime);
        subTime( &rateDiff, &mstDiff, &slvDiff);
        
        // Determines the number of 2^-32ns clock step adj / 8ns clock period based on the % of
        // error from the master clock per clock period.
        ptpClock->currRate = (int)((((double)rateDiff.seconds * 1000000000 + rateDiff.nanoseconds) / 
                             ((double)mstDiff.seconds * 1000000000 + mstDiff.nanoseconds)) * 8.0 * POW_2_32);
                             
        if ( abs(ptpClock->currRate) >= 0x4000000)
        {
            if ( ptpClock->currRate < 0) ptpClock->currRate = -0x3FFFFFF;
            else ptpClock->currRate = 0x3FFFFFF;
        }
                             
        // Keep a history of rate values for averaging purposes.
        ptpClock->rateHistory[ptpClock->rateSampleRateIdx] = ptpClock->currRate;
        ptpClock->rateSampleRateIdx += 1;
        if ( ptpClock->rateSampleRateIdx >= rtOpts->numRateSamples)
            ptpClock->rateSampleRateIdx = 0;
        
        ptpClock->numRateHistValues += 1;
        if ( ptpClock->numRateHistValues > rtOpts->numRateSamples)
            ptpClock->numRateHistValues = rtOpts->numRateSamples;
            
        DBG( "RATE SAMPLE: %d, sample #%d\n", ptpClock->currRate, ptpClock->numRateHistValues-1);
    }

    // Update the upper layers
    PTPUpdateStatus( STS_OFFSET_DATA, rtOpts, ptpClock);
    
    // Remember last sync tx/rx times
    subTime( &ptpClock->prevSyncRxTime, recv_time, &ptpClock->offset_from_master);
    subTime( &ptpClock->master_to_slave_delay, &ptpClock->master_to_slave_delay, &ptpClock->offset_from_master);
    ptpClock->prevSyncTxTime.seconds = send_time->seconds;
    ptpClock->prevSyncTxTime.nanoseconds = send_time->nanoseconds;
    
    return TRUE;
}


void updateClock(RunTimeOpts *rtOpts, PtpClock *ptpClock)
{
NS_BOOL negAdj;
long long val;
int x, avgRates, avgOfAvgsRate, deltaRate;

    DBG( "SYNC # %d\n", ptpClock->numSyncsSeen);
    
    if( ptpClock->offset_from_master.seconds)
    {
        // Reset the tuning variables if we have a large offset
        initClock( rtOpts, ptpClock);
    }

    if ( rtOpts->useTempRateFlag)
    {
        if ( ptpClock->numSyncsSeen < 3 || abs(ptpClock->lastRateAdj) == 0x3FFFFFF || abs(ptpClock->offset_from_master.nanoseconds) > 1000)
        {
            val = (long long)(ptpClock->offset_from_master.seconds * 1e9) + (long long)ptpClock->offset_from_master.nanoseconds;

            if ( rtOpts->clkOutEnableFlag && rtOpts->phaseAlignClkoutFlag)
            {
                // Step adj must be a multiple of the output clock period to keep the phase aligned
                val = (val / rtOpts->clkOutPeriod) * rtOpts->clkOutPeriod;
            }
            
            val -= 16;
            ptpClock->offset_from_master.seconds = (int)(val / 1e9);
            ptpClock->offset_from_master.nanoseconds = (int)(val % (long long)1e9);
            
            negAdj = TRUE;
            if ( val < 0)
                negAdj = FALSE;
            
            PTPClockStepAdjustment( rtOpts->eplPortHandle, abs(ptpClock->offset_from_master.seconds),
                                    abs(ptpClock->offset_from_master.nanoseconds), negAdj);
                                    
            ptpClock->waitingForAdjFlag = TRUE;
            
            DBG( "Step Adj offset from master: %ds %dns\n", ptpClock->offset_from_master.seconds,
                 ptpClock->offset_from_master.nanoseconds);
                 
            ptpClock->didStepFlag = TRUE;
        }
        else
            ptpClock->didStepFlag = FALSE;
        
        if ( ptpClock->numSyncsSeen >= 3 && !ptpClock->didStepFlag)  
        {
            deltaRate = (int)(((double)((double)ptpClock->offset_from_master.seconds * 1000000000L + (double)ptpClock->offset_from_master.nanoseconds) /
                              (((double)rtOpts->tempRateLength * 1000) / 8)) * POW_2_32);
           
            deltaRate = ptpClock->lastRateAdj - deltaRate;

            if ( abs(deltaRate) >= 0x4000000)
            {
                if ( deltaRate < 0) deltaRate = -0x3FFFFFF;
                else deltaRate = 0x3FFFFFF;
            }
            
            PTPClockSetRateAdjustment( rtOpts->eplPortHandle, (NS_UINT32)abs(deltaRate), TRUE,
                                       (deltaRate < 0) ? TRUE : FALSE);
                                       
            ptpClock->waitingForAdjFlag = TRUE;
            
            // Wait for temp rate to finish
            //TODO: implement
//            Sleep( rtOpts->tempRateLength / 1000);
            
            DBG( "Normal Rate: %d, Delta Rate: %d (%dns), Temp Rate: %d\n", ptpClock->lastRateAdj, deltaRate, ptpClock->offset_from_master.nanoseconds, ptpClock->lastRateAdj - deltaRate);
        }    
    }
    else
    {
        // Refine error offset using step adj. Determine how much to add/sub from the 
        // running clock based on difference from the master.
        DBG( "Step Adj offset from master: %ds %dns\n", ptpClock->offset_from_master.seconds,
             ptpClock->offset_from_master.nanoseconds);

        val = (long long)(ptpClock->offset_from_master.seconds * 1e9) + (long long)ptpClock->offset_from_master.nanoseconds;
        val -= 16;
        ptpClock->offset_from_master.seconds = (int)(val / 1e9);
        ptpClock->offset_from_master.nanoseconds = (int)(val % (long long)1e9);
        
        negAdj = TRUE;
        if ( val < 0)
            negAdj = FALSE;

        PTPClockStepAdjustment( rtOpts->eplPortHandle, abs(ptpClock->offset_from_master.seconds),
                                abs(ptpClock->offset_from_master.nanoseconds), negAdj);
                                
        ptpClock->waitingForAdjFlag = TRUE;
    }
    
    // Adjust the normal rate adjustment every so often
    if ( !rtOpts->syncEthMode && (ptpClock->numSyncsSeen == 2 || 
         (!ptpClock->ignoreNextRateFlag && ptpClock->numRateHistValues == rtOpts->numRateSamples)))
    {
        // Set the rate adj once the sample history has filled up. We keep an average of those averages
        // and that's used for the actual rate adj value.
        DBG( "numRateHistValues %d\n", ptpClock->numRateHistValues);
        
        avgRates = 0;
        for ( x = 0; x < ptpClock->numRateHistValues; x++)
        {
            DBG( "AVG SAMPLE: %d\n", ptpClock->rateHistory[x]);
            avgRates += ptpClock->rateHistory[x];
        }
        avgRates /= ptpClock->numRateHistValues;
        
        // Add this rate to the avg of avgs history.
        ptpClock->avgRatesHistory[ptpClock->avgRatesWriteIdx] = avgRates + ptpClock->lastRateAdj;
        ptpClock->avgRatesWriteIdx += 1;
        if ( ptpClock->avgRatesWriteIdx >= rtOpts->numRateAvgs)
            ptpClock->avgRatesWriteIdx = 0;
        
        ptpClock->numAvgRatesHistValues += 1;
        if ( ptpClock->numAvgRatesHistValues > rtOpts->numRateAvgs)
            ptpClock->numAvgRatesHistValues = rtOpts->numRateAvgs;
    
        // Calc the avg of avg's.
        avgOfAvgsRate = 0;
        for ( x = 0; x < ptpClock->numAvgRatesHistValues; x++)
        {
            avgOfAvgsRate += ptpClock->avgRatesHistory[x];
            DBG( "avgOfAvg %d, %d\n", x, ptpClock->avgRatesHistory[x]);
        }
        avgOfAvgsRate /= ptpClock->numAvgRatesHistValues;
        
        DBG( "Num avg of avgs %d, avg of avg %d\n", ptpClock->numAvgRatesHistValues, avgOfAvgsRate);
        
        if ( abs(avgOfAvgsRate) >= 0x4000000)
        {
            if ( avgOfAvgsRate < 0) avgOfAvgsRate = -0x3FFFFFF;
            else avgOfAvgsRate = 0x3FFFFFF;
        }

        ptpClock->lastRateAdj = avgOfAvgsRate;
        
        PTPClockSetRateAdjustment( rtOpts->eplPortHandle, (NS_UINT32)abs(ptpClock->lastRateAdj), FALSE,
                                   (ptpClock->lastRateAdj < 0) ? TRUE : FALSE);
                                   
        DBG( "Per 8ns new rate adj: %d\n", avgOfAvgsRate);
    }
    
    if ( !rtOpts->syncEthMode && ((ptpClock->numSyncsSeen == 3) || ptpClock->ignoreNextRateFlag) )
    {                                                                                    
        // Throw away the next rate adj measurement after a rate adj was made. This improves
        // the results.
        ptpClock->rateSampleRateIdx = 0;
        ptpClock->numRateHistValues = 0;
        ptpClock->ignoreNextRateFlag = FALSE;
    }
    
    if ( ptpClock->numRateHistValues == rtOpts->numRateSamples || ptpClock->numSyncsSeen == 2)
    {
        ptpClock->ignoreNextRateFlag = TRUE;
    }
    
    ptpClock->numSyncsSeen++;
    
    // If there is a large difference from the master we need to adjust the PPS trigger start time.
    if ( rtOpts->ppsEnableFlag && ptpClock->offset_from_master.seconds)
    {
        PTPCancelTrigger( rtOpts->eplPortHandle, 0);
        PTPArmTrigger( rtOpts->eplPortHandle, 0, ptpClock->prevSyncTxTime.seconds+1, 0, 
                       rtOpts->ppsRiseOrFallFlag, FALSE, 500000000, 500000000);
    }
    
    return;    
}

