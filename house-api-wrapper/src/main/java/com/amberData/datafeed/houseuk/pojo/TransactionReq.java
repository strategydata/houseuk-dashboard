package com.amberData.datafeed.houseuk.pojo;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Data
@Getter
@Setter
public class TransactionReq {
    private String minTransactionDate;
    private String maxTransactionDate;
    private String page;
}
