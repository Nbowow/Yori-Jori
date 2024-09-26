import styled from "styled-components";

export const LinkBanner = styled.div`
    display: flex;
    flex-direction: column;

    /* align-items: center; */

    box-sizing: border-box;
    padding: 100px;
    justify-content: center;
    gap: 8px;

    width: 100%;
    height: 243px;
    background-color: ${({ theme }) => theme.color.point.lightGreen};

    cursor: pointer;

    .title {
        font-family: "SUITSemiBold";
        font-size: ${({ theme }) => theme.fontSize.h3};
    }

    .text {
        font-family: "SUITMedium";
        font-size: ${({ theme }) => theme.fontSize.h4};
    }
`;
