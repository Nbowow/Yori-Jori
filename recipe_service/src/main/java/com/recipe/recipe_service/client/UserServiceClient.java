package com.recipe.recipe_service.client;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;

@FeignClient(name = "user-service")
public interface UserServiceClient {

    @GetMapping("/api/v1/users/id")
    Long getUserId(@RequestHeader("Authorization") String authorization);
}
