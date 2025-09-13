import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Container, Row, Col } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

function CreateUserPage() {
  const navigate = useNavigate();

  const [email, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [errors, setErrors] = useState("");

  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "email") setUsername(value);
    if (name === "password") setPassword(value);

    if (errors) setErrors("");
  };

  const handlePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      setErrors("Email and Password are required.");
      return;
    }

    const emailPattern = /^[a-zA-Z0-9._%+-]+@its\.jnj\.com$/;
    if (!emailPattern.test(email)) {
      setErrors("Email must be a valid JNJ email.");
      return;
    }

    setErrors("");

    try {
      const payload = {
        email,
        password,
        fullName: "",
      };
      const response = await fetch("http://localhost:9996/api/users/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setErrors(errorData.message || "Failed to sign up.");
      } else {
        const data = await response.json();
        console.log("Signup successful:", data);
        navigate("/admin/dashboard"); // Redirect or handle success
      }
    } catch (error) {
      setErrors("An error occurred while signing up.");
    }
  };
  const buttonStyle = {
    backgroundColor: "#eb1700",
    color: "white",
    border: "2px solid #b10018",
  };

  return (
    <Container class="container-fluid align-items-center">
      <Row className="justify-content-md-center mt-5">
        <Col xs={12} md={6}>
          <h2
            style={{
              display: "block",
              color: "#eb1700",
            }}
            clasclassName="text-center mb-4"
          >
            Add New User
          </h2>
          <br></br>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <input
                type="email"
                name="email"
                className="form-control"
                placeholder="JNJ email"
                value={email}
                onChange={handleChange}
                required
              />
            </div>
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
                value={password}
                onChange={handleChange}
                style={{ padding: "10px", width: "100%" }}
              />
              <FontAwesomeIcon
                icon={showPassword ? faEyeSlash : faEye}
                onClick={handlePasswordVisibility}
                style={{
                  position: "absolute",
                  right: "10px",
                  cursor: "pointer",
                }}
              />
            </div>

            {errors && <p style={{ color: "red" }}>{errors}</p>}
            <br></br>

            <Button style={buttonStyle} type="submit" className="w-100 mb-3">
              Register
            </Button>
          </form>
        </Col>
      </Row>
    </Container>
  );
}
export default CreateUserPage;
