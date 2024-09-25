import * as S from "./Banner.styled";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";

const Banner = ({ subTitle, title, navLink, imgUrl }) => {
    const navigate = useNavigate();

    return (
        <S.Banner>
            <S.ContentContainer>
                <S.ContentWrapper>
                    <S.TextSection>
                        <S.SubTitle>{subTitle}</S.SubTitle>
                        <S.Title>{title}</S.Title>
                    </S.TextSection>
                    <S.Link onClick={() => navigate(navLink)}>
                        <S.LinkText>레시피 보러가기</S.LinkText>
                        {">"}
                    </S.Link>
                </S.ContentWrapper>
                <S.Image src={imgUrl} />
            </S.ContentContainer>
        </S.Banner>
    );
};

Banner.propTypes = {
    subTitle: PropTypes.string,
    title: PropTypes.string,
    navLink: PropTypes.string,
    imgUrl: PropTypes.string,
};

export default Banner;
