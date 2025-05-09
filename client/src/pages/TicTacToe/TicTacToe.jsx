import "./TicTacToe.css";

const TicTacToe = () => {
    return (
        <div className="tic-tac-toe">
            <div className="board">
                {Array.from({ length: 16 }).map((_, index) => (
                    <div key={index} className="cell"></div>
                ))}
            </div>
            <div className="player-field">
                <input type="text" placeholder="Select a Player" className="player-input"/>
                <button className="give-up-button">Give Up?</button>
            </div>
        </div>
    );
};

export default TicTacToe;