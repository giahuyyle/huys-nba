import './Navbar.css';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="nav-links">
                <a href="/">
                    <img src="/src/assets/home.png" alt="Home" className="home"/>
                </a>
                
                <a href="https://www.linkedin.com/in/huylegia/" target="_blank" rel="noopener noreferrer">
                    <img src="/src/assets/linkedin.png" alt="LinkedIn" className="linkedin"/>
                </a>

                <a href="/">
                    <img src="src/assets/logo.png" alt="Logo" className="logo"/>
                </a>

                <a href="https://github.com/giahuyyle" target="_blank" rel="noopener noreferrer">
                    <img src="/src/assets/github.png" alt="GitHub" className="github"/>    
                </a>

                <a href="https://www.instagram.com/shot.chucker/?hl=en" target="_blank" rel="noopener noreferrer">
                    <img src="/src/assets/instagram.png" alt="Instagram" className="instagram"/>
                </a>
            </div>
        </nav>
    );
};

export default Navbar;