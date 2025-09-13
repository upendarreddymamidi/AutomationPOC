import { useState } from "react";
import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

function LoginPage() {
  const [loginData, setLoginData] = useState({ email: "", password: "" });
  const [loginError, setLoginError] = useState(""); // Use a string to store error message (empty means no error)
  const navigate = useNavigate(); // for programmatic navigation
  const [showPassword, setShowPassword] = useState(false);
  const [focus, setFocus] = useState({ email: false, password: false });

  const buttonHoverStyle = {
    backgroundColor: "#eb1700",
    color: "white",
    border: "2px solid #b10018",
    width: "150px",
  };
  const linkStyle = {
    fontSize: "14px",
    fontWeight: 400,
    color: "black",
    textDecoration: "none",
    transition: "color 0.3s, text-decoration 0.3s",
  };

  const linkHoverStyle = {
    color: "#eb1700",
    textDecoration: "underline",
  };

  const handleChange = (e) => {
    // Update form data state
    setLoginData({ ...loginData, [e.target.name]: e.target.value });
    // Clear any previous error message when user edits a field
    if (loginError) setLoginError("");
  };

  const handlePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send login request to backend API
      const response = await fetch("http://localhost:9996/api/users/auth", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginData), // send email and password as JSON
      });

      if (!response.ok) {
        // If response is not OK, determine error type
        if (response.status === 400) {
          // Invalid credentials (wrong email/password)
          setLoginError("Invalid email or password. Please try again.");
        } else {
          // Other errors (e.g., 500 server error)
          setLoginError(
            "An error occurred on the server. Please try again later."
          );
        }
      } else {
        // Successful login – parse the JSON to get token and user info
        const data = await response.json(); // { token: "...", user: { id, email } }
        // **Token Management**: store JWT (and user info) for future authenticated requests
        localStorage.setItem("authToken", data.token);
        localStorage.setItem("user", JSON.stringify(data.user));
        // You could also use cookies; for example, set a cookie with the token here if preferred.

        // Reset error (just in case) and redirect to the next page
        setLoginError("");
        data.user["email"] === "admin@its.jnj.com"
          ? navigate("/admin/dashboard")
          : navigate("/selections"); // Redirect to selections page after successful login
      }
    } catch (err) {
      // Network or unexpected error (e.g., server down)
      setLoginError(
        "Network error. Please check your connection and try again."
      );
    }
  };
  const handleFocus = (field) => {
    setFocus({ ...focus, [field]: true });
  };

  const handleBlur = (field) => {
    setFocus({ ...focus, [field]: false });
  };

  return (
    <Container className="container-fluid align-items-center">
      <Row className="justify-content-md-center mt-5">
        <Col xs={12} md={6}>
          <h2
            style={{
              textAlign: "left",
              display: "block",

              color: "#eb1700",
            }}
          >
            Test Data Automation Tool 
          </h2>
          <br></br>
          <Form onSubmit={handleSubmit}>
            {/* Email Field */}
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                name="email"
                placeholder="Enter JNJ email"
                pattern="[a-zA-Z0-9._]+@its\.jnj\.com"
                value={loginData.email}
                onChange={handleChange}
                onFocus={() => handleFocus("email")}
                onBlur={() => handleBlur("email")}
                required
                style={{
                  border: focus.email ? "2px solid black" : "1px solid #ced4da",
                  boxShadow: focus.email ? "0 0 1px black" : "none",
                  outline: "none", // Removes the default outline
                }}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <div
                className="mb-3"
                style={{
                  position: "relative",
                  display: "flex",
                  alignItems: "center",
                  margin: "10px auto",
                  width: "100%",
                }}
              >
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  className="form-control"
                  placeholder="Password"
                  value={loginData.password}
                  onChange={handleChange}
                  onFocus={() => handleFocus("password")}
                  onBlur={() => handleBlur("password")}
                  required
                  style={{
                    padding: "10px",
                    width: "100%",
                    border: focus.password
                      ? "2px solid black"
                      : "1px solid #ced4da",
                    boxShadow: focus.password ? "0 0 1px black" : "none",
                    outline: "none", // Removes the default outline
                  }}
                />
                {loginData.password.length > 0 && (
                  <FontAwesomeIcon
                    icon={showPassword ? faEyeSlash : faEye}
                    onClick={handlePasswordVisibility}
                    style={{
                      position: "absolute",
                      right: "10px",
                      cursor: "pointer",
                    }}
                  />
                )}
              </div>
            </Form.Group>
            <div className="d-flex justify-content-center">
              <Button
                style={buttonHoverStyle}
                type="submit"
                class="btn btn-primary btn-lg"
              >
                Login
              </Button>
            </div>
            {/* Links to Forgot Password / Signup (if any) */}
            <div className="mb-3 d-flex justify-content-between">
              <Link
                to="/ForgotPassword"
                style={linkStyle}
                onMouseEnter={(e) => {
                  Object.assign(e.target.style, linkHoverStyle);
                }}
                onMouseLeave={(e) => {
                  Object.assign(e.target.style, linkStyle);
                }}
              >
                Forgot Password?
              </Link>
              <Link
                to="/Signup"
                style={linkStyle}
                onMouseEnter={(e) => {
                  Object.assign(e.target.style, linkHoverStyle);
                }}
                onMouseLeave={(e) => {
                  Object.assign(e.target.style, linkStyle);
                }}
              >
                Sign Up
              </Link>
            </div>

            {/* Error Message Display */}
            {loginError && <p style={{ color: "red" }}>{loginError}</p>}
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default LoginPage;
