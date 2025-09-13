import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Container, Row, Button } from "react-bootstrap";
import axios from "axios";
import { FaEdit, FaTrash } from "react-icons/fa";
import Modal from "react-modal";

// Set the app element for accessibility
Modal.setAppElement("#root"); // Adjust this to your main app element

function AdminPage() {
  const [users, setUsers] = useState([]); // State to store user data
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [userIdToDelete, setUserIdToDelete] = useState(null); // State to store user ID for deletion

  const navigate = useNavigate();

  // Check if the user has admin privileges
  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user")); // Replace with actual key for user data
    if (user["email"] !== "admin@its.jnj.com") {
      alert("You do not have privilege to access this page.");
      navigate("/login"); // Redirect to login page
    } else {
      fetchUsers(); // Call fetchUsers if the user is admin
    }
  }, [navigate]);

  // Fetch users from backend
  const fetchUsers = async () => {
    try {
      const response = await axios.get("http://localhost:9996/api/users");
      console.log("API Response:", response.data); // Log the response
      setUsers(response.data);
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  };

  // Handle edit user
  const handleEdit = (userEmail) => {
    // Redirect to ResetPasswordAdmin page and pass email as state
    navigate("/resetpassword", { state: { userEmailId: userEmail } });
  };

  // Handle delete user
  const handleDelete = async (userId) => {
    try {
      await axios.delete(`http://localhost:9996/api/users/${userId}`); // Call delete API
      fetchUsers(); // Refresh the user list
    } catch (error) {
      console.error("Error deleting user:", error);
      alert("There was an error deleting the user.");
    }
  };

  // This function opens the modal and sets the user ID for deletion
  const openModal = (userId) => {
    setUserIdToDelete(userId);
    setModalIsOpen(true);
  };

  // This function closes the modal
  const closeModal = () => {
    setModalIsOpen(false);
    setUserIdToDelete(null); // Resetting user ID
  };

  // This function handles the confirmation of deletion
  const confirmDelete = () => {
    handleDelete(userIdToDelete);
    closeModal();
  };

  const buttonStyle = {
    backgroundColor: "#eb1700",
    color: "white",
    border: "2px solid #b10018",
  };

  // Custom modal styles
  const customModalStyles = {
    content: {
      top: "50%",
      left: "50%",
      right: "auto",
      bottom: "auto",
      marginRight: "-50%",
      transform: "translate(-50%, -50%)",
      width: "300px",
      padding: "20px",
      border: "none",
      borderRadius: "8px",
      backgroundColor: "#f8f9fa", // Light background color
      boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)", // Slight shadow
    },
  };

  // Render the component
  return (
    <Container>
      <Row className="justify-content-center mt-5">
        <div className="text-center mb-3">
          <h3 className="pb-2">User Management</h3>
          <Button
            style={buttonStyle}
            onClick={() => navigate("/CreateUser")}
            variant="success"
          >
            Add New User
          </Button>
        </div>
        {/* Dynamic Table */}
        <table className="table table-hover">
          <thead className="table-primary">
            <tr>
              <th scope="col">User ID</th>
              <th scope="col">Email Id</th>
              <th scope="col">Created At</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.length > 0 ? (
              users.map((user) => (
                <tr key={user.user_id}>
                  <th scope="row">{user.user_id}</th>
                  <td>{user.useremailid}</td>
                  <td>{new Date(user.created_at).toLocaleDateString()}</td>
                  <td>
                    <Button
                      variant="warning"
                      size="sm"
                      onClick={() => handleEdit(user.useremailid)}
                    >
                      <FaEdit style={{ marginRight: "5px" }} />
                      Edit
                    </Button>{" "}
                    <Button
                      variant="danger"
                      onClick={() => openModal(user.user_id)} // Open modal with user ID
                      size="sm"
                    >
                      <FaTrash style={{ marginRight: "5px" }} />
                      Delete
                    </Button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="text-center">
                  No users found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </Row>

      {/* Confirmation Modal */}
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Confirm Delete"
        style={customModalStyles} // Apply custom styles
      >
        <h2 style={{ textAlign: "center" }}>Confirm Deletion</h2>
        <p style={{ textAlign: "center" }}>
          Are you sure you want to delete this user?
        </p>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <button
            onClick={confirmDelete}
            style={{
              backgroundColor: "#eb1700",
              color: "white",
              border: "none",
              padding: "10px",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Yes, Delete
          </button>
          <button
            onClick={closeModal}
            style={{
              backgroundColor: "#ccc",
              color: "#333",
              border: "none",
              padding: "10px",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Cancel
          </button>
        </div>
      </Modal>
    </Container>
  );
}

export default AdminPage;
