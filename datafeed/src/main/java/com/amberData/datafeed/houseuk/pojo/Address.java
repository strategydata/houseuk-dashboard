package com.amberData.datafeed.houseuk.pojo;


import lombok.Data;

@Data
public class Address {
    
    private String id;

	private String poan;
	private String street;
	private String borough;
	private String county;
	private long listing;
    
    
}
