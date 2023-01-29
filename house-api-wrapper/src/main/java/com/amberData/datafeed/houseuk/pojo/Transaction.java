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
    
    private String id;

    private String transactionId;
    private String about;
    
    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDate transactionDate;
    private String pricePaid;
    private Boolean newBuild;
    private Enum<PropertyType> propertyType;
    private Enum<EstateType> estateType;
    private String hasTransaction;
    private Address propertyAddress;
    private String recordStatus;
}
