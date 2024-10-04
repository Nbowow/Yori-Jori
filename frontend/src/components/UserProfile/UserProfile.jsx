import * as S from "./UserProfile.styled";
import UserProfileImage from "./UserProfileImage/UserProfileImage";
import Button from "../Button/Button";
import PropTypes from "prop-types";
import { useNavigate } from "react-router-dom";
import { formatNumber } from "../../util/format-number";

const UserProfile = ({ showInfo, member }) => {
    const buttonText = "정보 수정";

    const follow = formatNumber(member.followers.length);
    const following = formatNumber(member.followings.length);

    const navigate = useNavigate();

    const onClickModifyButton = () => {
        navigate("/modify");
    };

    return (
        <S.UserProfile>
            <S.ProfileImage>
                <UserProfileImage imageUrl={member.profileImage} size="180px" />
            </S.ProfileImage>
            {showInfo && (
                <S.UserStat>
                    <S.TextWrapper>
                        <div className="nickname">{member.nickname}</div>
                        <div className="discription">{member.summary}</div>
                        <S.StatWrapper>
                            <S.Stat>
                                <div className="stat">팔로우</div>{" "}
                                <div>{follow}</div>
                            </S.Stat>
                            <S.Stat>
                                <div className="stat">팔로잉</div>{" "}
                                <div>{following}</div>
                            </S.Stat>
                        </S.StatWrapper>
                    </S.TextWrapper>
                    <Button
                        text={buttonText}
                        width="80px"
                        height="32px"
                        type="small"
                        onClick={onClickModifyButton}
                    />
                </S.UserStat>
            )}
        </S.UserProfile>
    );
};

const FollowerFollowingShape = PropTypes.shape({
    id: PropTypes.number,
    nickname: PropTypes.string,
    profileImage: PropTypes.string,
});

UserProfile.propTypes = {
    showInfo: PropTypes.bool,
    member: PropTypes.shape({
        profileImage: PropTypes.string,
        nickname: PropTypes.string,
        summary: PropTypes.string,
        followers: PropTypes.arrayOf(FollowerFollowingShape),
        followings: PropTypes.arrayOf(FollowerFollowingShape),
    }).isRequired,
};

export default UserProfile;
