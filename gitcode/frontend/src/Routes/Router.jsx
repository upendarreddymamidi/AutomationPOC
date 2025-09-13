import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import LoginPage from "../components/LoginPage.jsx";
import SelectionsPage from "../components/SelectionsPage.jsx";
import ResultsPage from "../components/ResultsPage.jsx";
import SignupPage from "../components/Signup.jsx";
import AdminDashboard from "../components/AdminDashboard.jsx";
import ForgotPasswordPage from "../components/ForgotPasswordPage.jsx";
import CreateUserPage from "../components/CreateUserPage.jsx";
import IntegrationTestResults from "../components/IntegrationTestResults.jsx";
import SelectedTemplatePage from "../components/SelectedTemplatePage.jsx";
import TestTemplatePage from "../components/TestTemplatePage.jsx";
import ReportViewer from "../components/ReportViewer.jsx";
import ResetPasswordAdmin from "../components/ResetPasswordAdmin.jsx";

function MainRouter(props) {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<Navigate replace to="/login" />} />
        <Route path="/selections" element={<SelectionsPage />} />
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/Signup" element={<SignupPage />} />
        <Route path="/ForgotPassword" element={<ForgotPasswordPage />} />
        <Route path="/CreateUser" element={<CreateUserPage />} />
        <Route path="/SelectedTemplate" element={<SelectedTemplatePage />} />
        <Route path="/ResetPassword" element={<ResetPasswordAdmin />} />
        <Route
          path="/integration-results"
          element={<IntegrationTestResults />}
        />
        <Route path="/TestTemplate" element={<TestTemplatePage />} />
        <Route path="/report-viewer" element={<ReportViewer />} />
      </Routes>
    </BrowserRouter>
  );
}

export default MainRouter;
