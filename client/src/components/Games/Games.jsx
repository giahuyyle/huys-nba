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
            <h2 className="games-title">Games</h2>
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
            <h2>More games are on the way!</h2>
        </div>
    );
};

export default Games;