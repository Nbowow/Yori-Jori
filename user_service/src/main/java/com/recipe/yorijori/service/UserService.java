package com.recipe.yorijori.service;

import com.recipe.yorijori.client.RecipeServiceClient;
import com.recipe.yorijori.client.SocialServiceClient;
import com.recipe.yorijori.data.domain.User;
import com.recipe.yorijori.data.dto.recipe.response.RecipeResponseDto;
import com.recipe.yorijori.data.dto.recipe.response.UserRecipeResponseDto;
import com.recipe.yorijori.data.dto.user.request.UserSignUpDto;
import com.recipe.yorijori.data.dto.user.response.FollowerResponseDto;
import com.recipe.yorijori.data.dto.user.response.FollowingResponseDto;
import com.recipe.yorijori.data.dto.user.response.UserResponseDto;
import com.recipe.yorijori.data.enums.Role;
import com.recipe.yorijori.repository.UserRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@Transactional
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final RecipeServiceClient recipeServiceClient;
    private final SocialServiceClient socialServiceClient;

    public void signUp(UserSignUpDto userSignUpDto) throws Exception {

        if (userRepository.findByEmail(userSignUpDto.getEmail()).isPresent()) {
            throw new Exception("이미 존재하는 이메일입니다.");
        }

        if (userRepository.findByNickname(userSignUpDto.getNickname()).isPresent()) {
            throw new Exception("이미 존재하는 닉네임입니다.");
        }

        User user = User.builder()
                .email(userSignUpDto.getEmail())
                .password(userSignUpDto.getPassword())
                .nickname(userSignUpDto.getNickname())
                .role(Role.USER)
                .build();

        user.passwordEncode(passwordEncoder);
        userRepository.save(user);
    }


    // 이메일을 기반으로 User 정보를 조회하고 DTO로 변환
    public UserResponseDto getUserByEmail(String email) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new IllegalArgumentException("사용자를 찾을 수 없습니다."));

        // User 객체를 UserDto로 변환하여 반환
        return new UserResponseDto(
                user.getEmail(),
                user.getNickname(),
                user.getProfileImage(),
                user.getName(),
                user.getSummary(), // 추가된 회원 한줄 소개
                getFollowers(user.getNickname()), // 추상 followers 정보
                getFollowings(user.getNickname()) // 추상 followings 정보
        );
    }

    public UserRecipeResponseDto getUserById(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("사용자를 찾을 수 없습니다."));

        List<RecipeResponseDto> recipeList = recipeServiceClient.getRecipes(userId);

        ModelMapper modelMapper = new ModelMapper();
        UserRecipeResponseDto userRecipeResponseDto = modelMapper.map(user, UserRecipeResponseDto.class);
        userRecipeResponseDto.setRecipes(recipeList);

        return userRecipeResponseDto;
    }

    public UserRecipeResponseDto getUserByNickname(String nickname) {
        User user = userRepository.findByNickname(nickname)
                .orElseThrow(() -> new IllegalArgumentException("사용자를 찾을 수 없습니다."));

        List<RecipeResponseDto> recipeList = recipeServiceClient.getRecipes(user.getUserId());

        ModelMapper modelMapper = new ModelMapper();
        UserRecipeResponseDto userRecipeResponseDto = modelMapper.map(user, UserRecipeResponseDto.class);
        userRecipeResponseDto.setRecipes(recipeList);

        return userRecipeResponseDto;
    }

    private List<FollowerResponseDto> getFollowers(String nickname) {

        List<FollowerResponseDto> followerResponseDtoList = socialServiceClient.getFollowers(nickname);
        ModelMapper modelMapper = new ModelMapper();


        return List.of();
    }

    private List<FollowingResponseDto> getFollowings(String nickname) {

        List<FollowingResponseDto> followingResponseDtoList = socialServiceClient.getFollowings(nickname);
        ModelMapper modelMapper = new ModelMapper();

        return List.of();
    }

    public Long getUserIdByEmail(String email) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new IllegalArgumentException("사용자를 찾을 수 없습니다."));
        return user.getUserId();
    }

}