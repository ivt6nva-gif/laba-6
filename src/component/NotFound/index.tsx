import type { FC } from "react";
import { Link } from "react-router-dom";

import s from "./style.module.css";

export const NotFoundPage: FC = () => {
  return (
    <div className={s.wrapper}>
      <div className={s.card}>
        <div className={s.code}>404</div>
        <h1 className={s.title}>Page not found</h1>

        <div className={s.actions}>
          <Link to="/login" className={s.secondary}>
            Login
          </Link>
        </div>

        <div className={s.ghost} aria-hidden="true">
          <div className={s.ghostBody}></div>
          <div className={s.ghostEyes}>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
  );
};