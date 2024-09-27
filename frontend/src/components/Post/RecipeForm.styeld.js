import styled from "styled-components";
export const Container = styled.div`
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    /* background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); */
`;

export const Title = styled.h1`
    font-size: ${({ theme }) => theme.fontSize.h1};
    color: #333;
    margin-bottom: 10px;
    font-family: "SUITEXTRABOLD";
`;

export const Form = styled.form`
    display: grid;
    grid-template-areas:
        "title title"
        "name image"
        "description image"
        "category image"
        "bottom none";
    gap: 20px;
`;

export const InputGroup = styled.div`
    grid-area: name;
    display: flex;
    flex-direction: column;
`;

export const InputGroup2 = styled.div`
    grid-area: description;
    display: flex;
    flex-direction: column;
`;

export const InputGroup3 = styled.div`
    grid-area: image;
    display: flex;
    flex-direction: column; /* 세로로 정렬 */
    align-items: center; /* 가운데 정렬 */
`;

export const InputGroup4 = styled.div`
    grid-area: category;
    display: flex;
    flex-direction: column;
`;

export const InputGroup5 = styled.div`
    display: flex;
    flex-direction: column;
`;

export const Label = styled.label`
    margin-bottom: 8px;
    font-family: "SUITSEMIBOLD";
    font-size: ${({ theme }) => theme.fontSize.h3};
`;

export const Input = styled.input`
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #f2f2f2;
`;

export const TextArea = styled.textarea`
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    height: 80px;
    resize: none;
    background-color: #f2f2f2;
`;

export const Select = styled.select`
    background-color: #f2f2f2;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: ${({ theme }) => theme.fontSize.text};
    font-family: "SUITREGULAR";
    color: ${({ theme }) => theme.color.gray.light};
`;

export const CategoryGroup = styled.div`
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
`;

export const ImageUploadButton = styled.label`
    display: flex;
    flex-direction: column; /* 세로로 정렬 */
    justify-content: center;
    align-items: center;
    border: 1px dashed #ccc;
    border-radius: 4px;
    padding: 20px;
    background-color: #f2f2f2;
    width: 300px;
    height: 300px;
    cursor: pointer;
    position: relative;
    margin: 20px 0;
    align-self: center; /* 가로 중앙 정렬 */
`;

export const ImagePreview = styled.img`
    width: 100%;
    height: auto;
    border-radius: 4px;
`;

export const BottomRow = styled.div`
    grid-area: bottom;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
`;

export const CloseButton = styled.button`
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    color: #ff0000;
    cursor: pointer;
    font-size: 16px;
`;

export const ButtonContainer = styled.div`
    text-align: center; /* 텍스트 중앙 정렬 */
`;

export const Text = styled.p`
    font-size: 22px;
    color: ${({ theme }) => theme.color.gray.light};
    margin-top: 10px;
    font-family: "SUITSEMIBOLD";
`;
