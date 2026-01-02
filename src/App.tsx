import type { FC } from "react";
import { Route, Routes, Navigate } from "react-router-dom";

import { Registration } from "./pages/Registration";
import { Login } from "./pages/Auth";
import { DashboardPage } from "./pages/Dashboard";
import { NotFound } from "./pages/404";

export const App: FC = () => {
  return (
    <Routes>
      {/* Редирект з кореня на логін */}
      <Route path="/" element={<Navigate to="/login" replace />} />

      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} />
      <Route path="/dashboard" element={<DashboardPage />} />

      {/* 404 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default App;