import "./Games.css"

const Games = () => {
    const games = [
        {
            id: 1,
            title: "NBA Tic-Tac-Toe",
            description: "The classic Tic-Tac-Toe game, but with NBA players!",
            image: "/src/assets/nba-tic-tac-toe.png",
            link: "/nba-tic-tac-toe"
        },
        {
            id: 2,
            title: "NBA Top 10",
            description: "A game that tests your knowledge of the top 10 of a given category.",
            image: "/src/assets/nba-top-10.png",
            link: "/nba-top-10"
        }
    ]

    return (
        <div className="games">
            <h1 className="games-title">Games</h1>
            <div className="games-list">
                {games.length > 0 ? (
                    games.map((game) => (
                        <a href={game.link} key={game.id} className="game-card">
                            <h2>{game.title}</h2>
                            <img src={game.image} alt={game.name} />
                            <p>{game.description}</p>
                        </a>
                    ))
                ) : (
                    <p>No games available</p>
                )}
            </div>
            <div className="games-footer">
                <p>© 2025 Huy Le. All rights reserved</p>
            </div>
        </div>
    );
};

export default Games;