package com.amberdata.datafeed.scheduler.datafeedscheduler;

import com.amberData.datafeed.houseuk.HouseApiWrapper;
import com.amberData.datafeed.houseuk.pojo.Transaction;
import com.amberData.datafeed.houseuk.pojo.TransactionReq;

import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.array;
import static org.hamcrest.Matchers.instanceOf;

@SpringBootTest
@Slf4j
class DatafeedSchedulerApplicationTests {

    @Autowired
    private HouseApiWrapper houseApiWrapper;

    @Test
    @DisplayName("syncTransaction")
    public void testDataFeedTask(){
        TransactionReq req = new TransactionReq();
        req.setPage("0");
        req.setMaxTransactionDate("2022-10-30");
        req.setMinTransactionDate("2022-10-30");
        Transaction[] transactions =houseApiWrapper.getAllTransaction(req);
        log.debug(String.valueOf(transactions));
        assertThat(transactions,array(instanceOf(Transaction.class)));
    }

//	@Test
//	void contextLoads() {
//	}

}
