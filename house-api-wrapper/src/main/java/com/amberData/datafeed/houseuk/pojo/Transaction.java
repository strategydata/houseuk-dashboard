package com.amberData.datafeed.houseuk.pojo;

import lombok.Data;
import java.time.LocalDate;

import com.fasterxml.jackson.annotation.JsonFormat;

@Data
public class Transaction {
    /*
     * the API reference is:
     * https://landregistry.data.gov.uk/app/root/doc/ppd
     * 
     * example:
     * http://landregistry.data.gov.uk/data/ppi/transaction/EED73E75-EA88-6AF3-E053-6C04A8C08ABA
     */


    private String transactionId;
    private String estateType;
    private Boolean newBuild;
    private Integer pricePaid;
    private Address propertyAddress;
    private String propertyType;
    private String recordStatus;
    private String transactionCategory;
    private String transactionDate;

}
