package com.amberData.datafeed.houseuk;

import io.netty.handler.timeout.ReadTimeoutHandler;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;

import org.springframework.http.*;

import reactor.core.publisher.Mono;

import com.amberData.datafeed.houseuk.pojo.Transaction;
import com.amberData.datafeed.houseuk.pojo.TransactionReq;

import java.time.Duration;
import java.util.concurrent.TimeUnit;

@Slf4j
public class HouseApiWrapper {

	@Value("${land-registry.base_url}")
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
		params.add("_page", transactionReq.getPage());
		params.add("min-transactionDate", transactionReq.getMinTransactionDate());
		params.add("max-transactionDate", transactionReq.getMaxTransactionDate());
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
				.bodyToMono(Transaction[].class)
				.timeout(Duration.ofSeconds(10));

		return body.block();
	}
}
