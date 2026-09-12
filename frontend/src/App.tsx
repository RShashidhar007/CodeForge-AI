import { BrowserRouter, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ProtectedRoute } from "./routes/ProtectedRoute";
import { RoleRoute } from "./routes/RoleRoute";
import { HomeRedirect } from "./routes/HomeRedirect";
import { MainLayout } from "./layouts/MainLayout";

import { LoginPage } from "./pages/auth/LoginPage";
import { RegisterPage } from "./pages/auth/RegisterPage";
import { CandidateDashboard } from "./pages/candidate/CandidateDashboard";
import { CandidateProfilePage } from "./pages/candidate/CandidateProfilePage";
import { RecruiterDashboard } from "./pages/recruiter/RecruiterDashboard";
import { RecruiterProfilePage } from "./pages/recruiter/RecruiterProfilePage";
import { AdminDashboard } from "./pages/admin/AdminDashboard";
import { AdminUsersPage } from "./pages/admin/AdminUsersPage";
import { UnauthorizedPage } from "./pages/UnauthorizedPage";
import { NotFoundPage } from "./pages/NotFoundPage";

import "./App.css";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/unauthorized" element={<UnauthorizedPage />} />

          {/* Any authenticated user reaches these; MainLayout renders the navbar */}
          <Route element={<ProtectedRoute />}>
            <Route element={<MainLayout />}>
              <Route path="/" element={<HomeRedirect />} />

              <Route element={<RoleRoute allowedRoles={["CANDIDATE"]} />}>
                <Route path="/candidate/dashboard" element={<CandidateDashboard />} />
                <Route path="/candidate/profile" element={<CandidateProfilePage />} />
              </Route>

              <Route element={<RoleRoute allowedRoles={["RECRUITER"]} />}>
                <Route path="/recruiter/dashboard" element={<RecruiterDashboard />} />
                <Route path="/recruiter/profile" element={<RecruiterProfilePage />} />
              </Route>

              <Route element={<RoleRoute allowedRoles={["ADMIN"]} />}>
                <Route path="/admin/dashboard" element={<AdminDashboard />} />
                <Route path="/admin/users" element={<AdminUsersPage />} />
              </Route>
            </Route>
          </Route>

          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
