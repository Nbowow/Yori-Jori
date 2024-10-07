import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import RecipeUser from "../../components/RecipeDetail/RecipeUser/RecipeUser";
import RecipeHeader from "../../components/RecipeDetail/RecipeHeader/RecipeHeader";
import RecipeStep from "../../components/RecipeStep/RecipeStep";
import RecipeInfo from "../../components/RecipeDetail/RecipeInfo";
import Comments from "../../components/Comment/Comments";
import Review from "../../components/Review/Review";
import * as S from "./RecipeDetail.styled";
import { getRecipe, getReviews, getComments } from "../../api/recipe";

const RecipeDetail = () => {
    const [recipe, setRecipes] = useState({});
    const [reviews, setReviews] = useState([]);
    const [comments, setComments] = useState([]);
    const { id } = useParams();

    useEffect(() => {
        const fetchRecipe = async () => {
            const data = await getRecipe(id);
            setRecipes(data);
        };
        const fetchReview = async () => {
            const data = await getReviews(id);
            setReviews(data);
        };
        const fetchComment = async () => {
            const data = await getComments(id);
            setComments(data);
        };
        fetchRecipe(id);
        fetchReview(id);
        fetchComment(id);
    }, [id]);

    const allergies = ["토마토", "우유"];

    const user = {
        id: 1,
        imgUrl: "https://mblogthumb-phinf.pstatic.net/MjAyMTAzMjJfMjUg/MDAxNjE2Mzg4ODI3MzMx.0G6S0UjP07n30LGB4ckxTy61yx06j23nvkKxD0J3cPUg.-kIS_AzileIuNGaJ7W_-eCIVIzuKC9VmErz7zoFpDNUg.JPEG.chooddingg/E4DE992B-B5DF-44F2-AA60-E7F9D00B8BEE-16837-0000081DF5EE03C2_file.jpg?type=w800",
        name: "명수옹",
        followCnt: 100,
        talk: " 명수옹의 요리조리요리조리요리조리요리조리",
    };

    const step = [
        {
            img: "https://cdn.pixabay.com/photo/2021/07/19/16/04/pizza-6478478_1280.jpg",
            text: "밀가루, 소금, 설탕, 이스트를 넣고 섞어주세요.",
        },
        {
            img: "https://cdn.pixabay.com/photo/2021/07/19/16/04/pizza-6478478_1280.jpg",
            text: "밀가루, 소금, 설탕, 이스트를 넣고 섞어주세요.",
        },
    ];

    const rating = [100, 50, 30, 1, 5];
    return (
        <>
            <S.Container>
                <S.InfoSection>
                    <RecipeHeader recipe={recipe} />
                    {/* todo: RecipeInfo 컴포넌트에 allergies props전달 */}
                    <RecipeInfo recipe={recipe} allergies={allergies} />
                </S.InfoSection>

                <S.StepSection>
                    {/* todo: RecipeStep 컴포넌트에 step props 전달 */}
                    <RecipeStep recipe={step} />
                </S.StepSection>

                <S.UserSection>
                    {/* todo : recipeUser 컴포넌트에 user props 전달 */}
                    <RecipeUser user={user} />
                </S.UserSection>

                <Review reviews={reviews} rating={rating} recipe={recipe} />
                <S.CommentSection>
                    <S.CommentTitle>댓글 {comments.length}개</S.CommentTitle>
                    <Comments initComments={comments} id={id} />
                </S.CommentSection>
            </S.Container>
        </>
    );
};

export default RecipeDetail;
