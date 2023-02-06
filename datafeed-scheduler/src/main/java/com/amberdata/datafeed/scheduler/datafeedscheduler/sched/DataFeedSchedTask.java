package com.amberdata.datafeed.scheduler.datafeedscheduler.sched;

import com.amberData.datafeed.houseuk.HouseApiWrapper;
import com.amberData.datafeed.houseuk.pojo.Transaction;
import com.amberData.datafeed.houseuk.pojo.TransactionReq;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Autowired;


@Component
@Slf4j
public class DataFeedSchedTask {
    @Autowired
    private HouseApiWrapper houseApiWrapper;

//    @Autowired
//    private MongoTemplate template;

    @Scheduled(initialDelay = 1000*0,fixedDelay = 1000*60*5)
    public void syncTransaction(){
        log.info("Start sync transaction data ");
        Transaction[] transactions =houseApiWrapper.getAllTransaction(new TransactionReq());
        if(transactions !=null && transactions.length >0){
            for(Transaction tran:transactions){
                log.info("this is tran",tran);

            }
        }

    }

}
