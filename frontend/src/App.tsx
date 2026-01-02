import type { FC } from "react";
import { Route, Routes } from "react-router-dom";
import { Registration } from "./pages/Registration";
import { Login } from "./pages/Auth";
import { DashboardPage } from "./pages/Dashboard";
import { NotFound } from "./pages/404";

export const App: FC = () => {
  return (
  <>
  <main>
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  </main>
  </>);};
  
export default App;