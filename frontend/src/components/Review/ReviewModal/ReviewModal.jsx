import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import ReviewOverview from "../ReviewOverview/ReviewOverview";
import Review from "../ReviewDetail/ReviewDetail";
import * as S from "./ReviewModal.styled";

const ReviewModal = ({ recipe, reviews }) => {
    const [selectedReviewId, setSelectedReviewId] = useState(null);

    useEffect(() => {
        if (reviews.length > 0) {
            setSelectedReviewId(0);
        }
    }, [reviews]);

    const changeReview = (idx) => {
        setSelectedReviewId(idx);
    };

    return (
        <S.ReviewModalWrapper>
            {selectedReviewId !== null && (
                <>
                    <S.Reviews>
                        {reviews.map((review, idx) => (
                            <ReviewOverview
                                key={review.id}
                                onClick={() => changeReview(idx)}
                                review={review}
                                isSelected={idx === selectedReviewId}
                            />
                        ))}
                    </S.Reviews>

                    <Review
                        review={reviews[selectedReviewId]}
                        recipe={recipe}
                    />
                </>
            )}
        </S.ReviewModalWrapper>
    );
};

ReviewModal.propTypes = {
    recipe: PropTypes.object.isRequired,
    reviews: PropTypes.array.isRequired,
};
export default ReviewModal;