import React, { useState } from "react";
import s from "./style.module.css";
import type { IFormAuth } from "../../interfaces/forms";
import { login } from "../../api/auth/login";
import { Routes } from "../../enums/routes";
import { useNavigate } from "react-router-dom";

export const LoginForm = () => {
    const [userForm, setUserForm] = useState<IFormAuth>({
    username: "",
    password: "",});

const [error, setError] = useState<string | null>(null);
const navigation = useNavigate();

const handleClick = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setUserForm((prev: any) => ({ ...prev, [name]: value }));};

const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await login(userForm);
    console.log(result);
    if ("error" in result) {
        setError("Incorrect password/login");}
    else {
        navigation(Routes.DASHBOARD);}
};

return (
    <div className={s.wrapper}>
        <div className={s.card}>
        <h2 className={s.title}>Authorization</h2>
        <p className={s.subtitle}>Log in or register to continue.</p>

    <div className={s.fields}>

<input
    name="username"
    type="text"
    placeholder="Username"
    className={s.input}
    value={userForm.username}
    onChange={handleClick}
/>

<input
    name="password"
    type="password"
    placeholder="Password"
    value={userForm.password}
    className={s.input}
    onChange={handleClick}
/>

</div>
    <button className={s.button} onClick={handleSubmit}>
    Continue
</button>

<p className={s.hint}>
    Use a strong password that you don&apos;t reuse on other services.
</p>

{error && (
    <p className={s.hint} style={{ color: "#f97373" }}>
{error}
</p>

)}
</div>
</div>
);
};