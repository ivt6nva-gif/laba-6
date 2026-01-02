import { Link } from "react-router-dom";
import s from "./style.module.css";

export const NavBarAuth = () => {
    return (
<nav className={s.nav}>
<Link to="/login" className={s.link}>
Login
</Link>
<Link to="/registration" className={s.link}>
Registration
</Link>
</nav>
);
};