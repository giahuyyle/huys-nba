import "./Top10.css";
import { useEffect, useState } from "react";
import api from "../../utils/api";
import teams from "../../utils/Teams";

const teamKeys = Object.keys(teams);

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

const Top10 = () => {
    const [input, setInput] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [top10Players, setTop10Players] = useState(Array(10).fill(null));

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

    return (
        <div className="top-10">
            <div className="top10-boxes">
                {[...Array(10)].map((_, i) => {
                    const player = mock_Top10[i];
                    const TeamLogo = player && player.team ? teams[player.team] : null;

                    return (
                        <div className="top10-box" key={i}>
                            <span className="number-box">{i+1}.</span>
                            <span className="player-team">
                                {TeamLogo && <TeamLogo size={32} />}
                            </span>
                            <span className="player-box">
                                {player.name}
                                { /* TO-DO: implement correct players or not */}
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
                            <li key={player.id}>
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