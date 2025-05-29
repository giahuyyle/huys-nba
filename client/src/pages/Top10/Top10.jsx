import "./Top10.css";
import { useEffect, useState } from "react";
import api from "../../utils/api";
import { teamNicknames, teamAbbreviations } from "../../utils/Teams";

/*
const mock_Top10 = [
    { id: 1, name: "LeBron James", team: "lakers" },
    { id: 2, name: "Kevin Durant", team: "suns" },
    { id: 3, name: "Stephen Curry", team: "warriors" },
    { id: 4, name: "Giannis Antetokounmpo", team: "bucks" },
    { id: 5, name: "Luka Doncic", team: "lakers" },
    { id: 6, name: "Kawhi Leonard", team: "clippers" },
    { id: 7, name: "James Harden", team: "clippers" },
    { id: 8, name: "Nikola Jokic", team: "nuggets" },
    { id: 9, name: "Joel Embiid", team: "sixers" },
    { id: 10, name: "Jimmy Butler", team: "warriors" }
]
*/

const Top10 = () => {
    const [input, setInput] = useState("");
    const [todayTitle, setTodayTitle] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [mockTop10, setMockTop10] = useState([]);
    const [top10Players, setTop10Players] = useState(Array(10).fill(null));
    const [listName, setListName] = useState("");
    const [helper, setHelper] = useState("Select a Player");

    //setTodayTitle("PPG Leaders of the 24/25 season");

    useEffect(() => {
        const fetchPlayers = async () => {
            if (input.trim() === "" || input.length < 3) {
                setSuggestions([]);
                return;
            }
            try {
                const response = await api.get(`/players/${encodeURIComponent(input)}`);
                setSuggestions(response.data || []);
            } catch (err) {
                setSuggestions([]);
            }
        };
        const timeout = setTimeout(fetchPlayers, 300);
        return () => clearTimeout(timeout);
    }, [input]);

    useEffect(() => {
        const fetchTop10 = async () => {
            try {
                const response = await api.get("/top10?date=29may2025");
                setMockTop10(response.data || []);
            } catch (err) {
                setMockTop10([]);
            }
        };
        fetchTop10();
        setTodayTitle("PPG Leaders of the 24/25 season");
    }, []);

    // Example handler for selecting a player
    const handleSelectPlayer = (selectedPlayer) => {
        const idx = mockTop10.findIndex(
            p => p.name.toLowerCase() === selectedPlayer.name.toLowerCase()
        );
        if (idx !== -1 && !top10Players[idx]) {
            const updated = [...top10Players];
            updated[idx] = selectedPlayer;
            setTop10Players(updated);
            setHelper(`You guessed ${selectedPlayer.name} correctly!`);
        } else if (idx !== -1 && top10Players[idx]) {
            setHelper(`${selectedPlayer.name} is already guessed`);
            setInput("");
            setSuggestions([]);
        } else {
            setHelper(`${selectedPlayer.name} is not on the list`);
        }
        setInput("");
        setSuggestions([]);
    };

    return (
        <div className="top-10">
            <div className="top10-boxes">
                <h3 className="helper-text">{helper}</h3>
                <h3 className="todays-title">Today's Topic: {todayTitle}</h3>
                {[...Array(10)].map((_, i) => {
                    const player = mockTop10[i];
                    const guessedPlayer = top10Players[i];
                    const TeamLogo = player && player.team ? teamAbbreviations[player.team] : null;

                    return (
                        <div
                            className={`top10-box${guessedPlayer ? " correct" : ""}`}
                            key={i}
                        >
                            <span className="number-box">{i + 1}.</span>
                            <span className="player-team">
                                {TeamLogo && <TeamLogo size={32} />}
                            </span>
                            <span className="player-box">
                                {guessedPlayer ? guessedPlayer.name : ""}
                            </span>
                        </div>
                    );
                })}
            </div>
            <div className="player-field">
                <input
                    type="text"
                    placeholder="Select a Player"
                    className="player-input"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    autoComplete="off"
                />
                <button className="give-up-button">Give Up?</button>
                {suggestions.length > 0  && (
                    <ul className="suggestions-list">
                        {suggestions.map((player) => (
                            <li key={player.id} onClick={() => handleSelectPlayer(player)}>
                                {player.name}
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default Top10;