function getRatioBy(type, height) {
    switch (type) {
        case "inactive_heart":
        case "active_heart":
            return (height * 16) / 15;
        case "inactive_bookmark":
        case "active_bookmark":
            return (height * 12) / 15;
        case "comment":
            return height;
        default:
            return 0;
    }
}

export function getButtonIcon(type, height = "15px") {
    const width = getRatioBy(type, parseFloat(height)) + "px";

    switch (type) {
        case "inactive_heart":
            return (
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width={width}
                    height={height}
                    viewBox="0 0 16 15"
                    fill="none"
                >
                    <path
                        d="M8.08 12.7112L8 12.7929L7.912 12.7112C4.112 9.18801 1.6 6.85831 1.6 4.49591C1.6 2.86104 2.8 1.63488 4.4 1.63488C5.632 1.63488 6.832 2.45232 7.256 3.56403H8.744C9.168 2.45232 10.368 1.63488 11.6 1.63488C13.2 1.63488 14.4 2.86104 14.4 4.49591C14.4 6.85831 11.888 9.18801 8.08 12.7112ZM11.6 0C10.208 0 8.872 0.662125 8 1.70027C7.128 0.662125 5.792 0 4.4 0C1.936 0 0 1.97003 0 4.49591C0 7.57766 2.72 10.1035 6.84 13.921L8 15L9.16 13.921C13.28 10.1035 16 7.57766 16 4.49591C16 1.97003 14.064 0 11.6 0Z"
                        fill="#4CAC67"
                    />
                </svg>
            );
        case "active_heart":
            return (
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width={width}
                    height={height}
                    viewBox="0 0 16 15"
                    fill="none"
                >
                    <path
                        d="M8 15L6.84 13.921C2.72 10.1035 0 7.57766 0 4.49591C0 1.97003 1.936 0 4.4 0C5.792 0 7.128 0.662125 8 1.70027C8.872 0.662125 10.208 0 11.6 0C14.064 0 16 1.97003 16 4.49591C16 7.57766 13.28 10.1035 9.16 13.921L8 15Z"
                        fill="#4CAC67"
                    />
                </svg>
            );
        case "inactive_bookmark":
            return (
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width={width}
                    height={height}
                    viewBox="0 0 12 15"
                    fill="none"
                >
                    <path
                        d="M0.75 0H11.25C11.4489 0 11.6397 0.076554 11.7803 0.212821C11.921 0.349088 12 0.533906 12 0.726616V14.6362C12.0001 14.7012 11.9822 14.765 11.9482 14.821C11.9142 14.877 11.8653 14.9231 11.8066 14.9546C11.7479 14.986 11.6816 15.0017 11.6146 14.9999C11.5476 14.9981 11.4823 14.9789 11.4255 14.9443L6 11.6477L0.5745 14.9436C0.517776 14.9781 0.452541 14.9973 0.385576 14.9991C0.318612 15.001 0.252365 14.9854 0.193721 14.954C0.135078 14.9226 0.0861801 14.8766 0.0521121 14.8207C0.0180441 14.7648 4.98531e-05 14.7011 0 14.6362V0.726616C0 0.533906 0.0790178 0.349088 0.21967 0.212821C0.360322 0.076554 0.551088 0 0.75 0ZM10.5 1.45323H1.5V12.6664L6 9.93357L10.5 12.6664V1.45323Z"
                        fill="#4CAC67"
                    />
                </svg>
            );
        case "active_bookmark":
            return (
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width={width}
                    height={height}
                    viewBox="0 0 12 15"
                    fill="none"
                >
                    <path
                        d="M0.75 0H11.25C11.4489 0 11.6397 0.076554 11.7803 0.212821C11.921 0.349088 12 0.533906 12 0.726616V14.6362C12.0001 14.7012 11.9822 14.765 11.9482 14.821C11.9142 14.877 11.8653 14.9231 11.8066 14.9546C11.7479 14.986 11.6816 15.0017 11.6146 14.9999C11.5476 14.9981 11.4823 14.9789 11.4255 14.9443L6 11.6477L0.5745 14.9436C0.517776 14.9781 0.452541 14.9973 0.385576 14.9991C0.318612 15.001 0.252365 14.9854 0.193721 14.954C0.135078 14.9226 0.0861801 14.8766 0.0521121 14.8207C0.0180441 14.7648 4.98531e-05 14.7011 0 14.6362V0.726616C0 0.533906 0.0790178 0.349088 0.21967 0.212821C0.360322 0.076554 0.551088 0 0.75 0Z"
                        fill="#4CAC67"
                    />
                </svg>
            );
        case "comment":
            return (
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width={width}
                    height={height}
                    viewBox="0 0 15 15"
                    fill="none"
                >
                    <path
                        d="M0 2.90199C0 2.13233 0.282206 1.3942 0.784535 0.849972C1.28686 0.305744 1.96817 0 2.67857 0H12.3214C13.0318 0 13.7131 0.305744 14.2155 0.849972C14.7178 1.3942 15 2.13233 15 2.90199V8.70596C15 9.08705 14.9307 9.46442 14.7961 9.8165C14.6615 10.1686 14.4642 10.4885 14.2155 10.758C13.9667 11.0274 13.6715 11.2412 13.3465 11.387C13.0215 11.5329 12.6732 11.6079 12.3214 11.6079H8.23714L4.95536 14.7189C4.8035 14.8627 4.61663 14.9561 4.41708 14.9879C4.21753 15.0197 4.01375 14.9885 3.8301 14.8982C3.64646 14.8078 3.49072 14.6621 3.38151 14.4784C3.2723 14.2946 3.21425 14.0807 3.21429 13.8622V11.6079H2.67857C1.96817 11.6079 1.28686 11.3022 0.784535 10.758C0.282206 10.2137 0 9.47561 0 8.70596V2.90199ZM2.67857 1.16079C2.25233 1.16079 1.84355 1.34424 1.54215 1.67078C1.24075 1.99731 1.07143 2.44019 1.07143 2.90199V8.70596C1.07143 9.16775 1.24075 9.61063 1.54215 9.93717C1.84355 10.2637 2.25233 10.4472 2.67857 10.4472H4.28571V13.8111L7.83429 10.4472H12.3214C12.7477 10.4472 13.1565 10.2637 13.4578 9.93717C13.7592 9.61063 13.9286 9.16775 13.9286 8.70596V2.90199C13.9286 2.44019 13.7592 1.99731 13.4578 1.67078C13.1565 1.34424 12.7477 1.16079 12.3214 1.16079H2.67857Z"
                        fill="#4CAC67"
                    />
                </svg>
            );
        default:
            return <div>non-type</div>;
    }
}
