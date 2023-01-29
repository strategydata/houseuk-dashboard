package com.amberData.datafeed.houseuk;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;

import org.springframework.http.*;

import reactor.core.publisher.Mono;

import com.amberData.datafeed.houseuk.pojo.Transaction;
import com.amberData.datafeed.houseuk.pojo.TransactionReq;

@Slf4j
public class HouseukApplication {

	@Value("${landregistry.base_url}")
	private String baseUrl;

	private WebClient webClient;

	@PostConstruct
	public void init() {
		webClient = WebClient.builder().baseUrl(baseUrl).build();
	}

	public Transaction[] getAllTransaction(TransactionReq transactionReq) {
		MultiValueMap<String, String> headers = new LinkedMultiValueMap<>();
		headers.add("Host", baseUrl);

		MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
		params.add("_page", "0");
		params.add("min-transactionDate", "2022-11-01");
		params.add("max-transactionDate", "2022-11-30");
		Mono<Transaction[]> body = webClient
				.get()
				.uri((urlBuilder) -> {
					return urlBuilder
							.path("/data/ppi/transaction-record.json")
							.queryParams(params)
							.build();
				})
				.retrieve()
				.onStatus(HttpStatusCode::is4xxClientError, clientResponse -> {
					log.error("Error when getAllTransaction: ", clientResponse);
					return Mono.error(new Exception(clientResponse.toString()));
				})
				.bodyToMono(Transaction[].class);

		return body.block();
	}
}
