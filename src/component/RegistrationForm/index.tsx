import { useState } from "react";
import s from "./style.module.css";
import { register } from "../../api/auth/registration";
import { useNavigate } from "react-router-dom";
import { Routes } from "../../enums/routes";

export const RegistrationForm: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [repeatPassword, setRepeatPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);

    if (!username || !password || !repeatPassword) {
      setError("Fill all inputs");
      return;
    }

    if (password !== repeatPassword) {
      setError("Password doesn't match");
      return;
    }

    const result = await register({ username, password });

    if ("error" in result) {
      if (result.status === 409) {
        setError("User already exist");
      } else {
        setError(result.error);
      }
    } else {
      alert("Успішно зареєстровано!");
      setTimeout(() => {
        navigate(Routes.LOGIN);
      }, 5000);
    }
  };

  return (
    <div className={s.wrapper}>
      <form className={s.card} onSubmit={handleSubmit}>
        <h2 className={s.title}>Registration</h2>
        <p className={s.subtitle}>Create new account.</p>

        <div className={s.fields}>
          <input
            name="username"
            type="text"
            placeholder="Username"
            className={s.input}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            name="password"
            type="password"
            placeholder="Password"
            className={s.input}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <input
            name="repeatPassword"
            type="password"
            placeholder="Repeat password"
            className={s.input}
            value={repeatPassword}
            onChange={(e) => setRepeatPassword(e.target.value)}
          />
        </div>

        <button className={s.button} type="submit">
          Registration
        </button>

        {error && (
          <p className={s.hint} style={{ color: "#f97373" }}>
            {error}
          </p>
        )}
      </form>
    </div>
  );
};