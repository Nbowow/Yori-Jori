package com.recipe.recipe_service.repository;

import com.recipe.recipe_service.data.domain.Recipe;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RecipeRepository extends JpaRepository<Recipe, Integer> {

    Iterable<Recipe> findByUserId(Long userId);
}
