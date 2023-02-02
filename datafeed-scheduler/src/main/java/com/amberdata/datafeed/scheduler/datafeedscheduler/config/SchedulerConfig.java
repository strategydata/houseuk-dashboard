package com.amberdata.datafeed.scheduler.datafeedscheduler.config;

import org.springframework.context.annotation.Configuration;

import com.amberData.datafeed.houseuk.HouseApiWrapper;

import org.springframework.context.annotation.Bean;



@Configuration
public class SchedulerConfig{

    @Bean
    public HouseApiWrapper houseApiWrapper(){
        return new HouseApiWrapper();
    }
}