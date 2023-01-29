package com.amberData.datafeed.houseuk.pojo;

import lombok.Data;

@Data
public class TransactionReq {
    private String minTransactionDate;
    private String maxTransactionDate;
    private String page;
}
