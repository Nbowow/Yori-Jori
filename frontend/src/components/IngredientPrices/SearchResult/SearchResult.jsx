import PropTypes from "prop-types";
import { useState } from "react";
import { getIngredientPrices } from "../../../api/ingredientApi";
import InteractionToggle from "../../Toggle/InteractionToggle/InteractionToggle";
import Button from "../../Button/Button";
import * as S from "./SearchResult.styled";
import YearlyPriceChart from "../YearlyPriceChart/YearlyPriceChart";
import LowestPrices from "../LowestPrice/LowestPrices";

const SearchResult = ({ result, onLike, like }) => {
    const [showInfo, setShowInfo] = useState(false);
    const [priceHistory, setPriceHistory] = useState();
    const handleClick = async () => {
        const data = await getIngredientPrices(result.id);
        setPriceHistory(data);
        setShowInfo((prev) => !prev);
    };
    return (
        <S.Wrapper>
            {result.name !== "Unknown" ? (
                <>
                    <S.ResultWrapper>
                        <S.ResultInfo>
                            <S.Img
                                src={result.ingredientImage}
                                alt="ingredient"
                            />
                            <S.Label>
                                <S.Name>{result.name}</S.Name>
                            </S.Label>
                            <Button
                                text="자세히 보기"
                                onClick={() => handleClick()}
                            />
                        </S.ResultInfo>
                        <InteractionToggle
                            isActive={like}
                            onClick={() => onLike(result)}
                            type="heart"
                            size="1.5rem"
                        />
                    </S.ResultWrapper>

                    {showInfo && (
                        <S.MoreInfo show={showInfo}>
                            <YearlyPriceChart priceHistory={priceHistory} />
                            <LowestPrices name={result.name} />
                        </S.MoreInfo>
                    )}
                </>
            ) : (
                <div>검색 결과가 없습니다</div>
            )}
        </S.Wrapper>
    );
};

SearchResult.propTypes = {
    result: PropTypes.object.isRequired,
    onLike: PropTypes.func,
    like: PropTypes.bool,
};
export default SearchResult;
