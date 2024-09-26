import * as S from "./UserProfileStat.styled";
import Button from "../../Button/Button";
import PropTypes from "prop-types";

import { formatNumber } from "../../../util/format-number";

const UserProfileStat = ({ nickName, discription }) => {
    // TODO: 회원 정보에 따라서 값 변경하기
    const buttonText = "수정";
    const followerCount = formatNumber(12300000);
    const followingCount = formatNumber(5);

    return (
        <>
            <S.ProfileText>
                <S.NickName>{nickName}</S.NickName>
                <S.Description>{discription}</S.Description>
                <S.Stat>
                    {/* TODO: 클릭시 모달 */}
                    <div>
                        <div className="bold">팔로워</div>
                        <div>{followerCount}</div>
                    </div>
                    <div>
                        <div className="bold">팔로잉</div>
                        <div>{followingCount}</div>
                    </div>
                </S.Stat>
            </S.ProfileText>
            <S.ProfileButton>
                <Button width="93px" height="40px" text={buttonText} />
            </S.ProfileButton>
        </>
    );
};

UserProfileStat.propTypes = {
    nickName: PropTypes.string,
    discription: PropTypes.string,
};

export default UserProfileStat;