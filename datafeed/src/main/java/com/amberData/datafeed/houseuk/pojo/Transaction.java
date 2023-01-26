package com.amberData.datafeed.houseuk.pojo;

import lombok.Data;

@Data
public class Transaction {
    private String id;

    private String transactionId;
    private String about;
    private String transactionDate;
    private String pricePaid;
    private Boolean newBuild;
    private Enum<PropertyType> propertyType;
    private Enum<EstateType> estateType;
    private String hasTransaction;
    private Address propertyAddress;
    private String recordStatus;
}
