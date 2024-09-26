import styled from "styled-components";
import { flexAroundStyle, flexStartStyle } from "../../../styles/common";

export const Reviews = styled.div`
    ${flexStartStyle}
    flex-direction: column;
    height: 90%;
    width: 50%;
    overflow: auto;
    padding: 1rem;
`;
export const ReviewModalWrapper = styled.div`
    ${flexAroundStyle}
    height: 100%;
    width: 100%;
`;