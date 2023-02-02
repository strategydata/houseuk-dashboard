package com.amberdata.datafeed.scheduler.datafeedscheduler.sched;

import com.amberData.datafeed.houseuk.HouseApiWrapper;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Autowired;


@Component
public class DataFeedSchedTask {
    @Autowired
    private HouseApiWrapper houseApiWrapper;


}
