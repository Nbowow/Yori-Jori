package com.recipe.recipe_service.data.dto.user;

import lombok.Data;

@Data
public class UserSimpleResponseDto {
    private Long userId;
    private String profileImage;
    private String nickname;
}
