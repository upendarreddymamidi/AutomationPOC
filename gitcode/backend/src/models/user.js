import bcrypt from "bcryptjs";
import { pool } from "../app.js";

export const createUser = async ({ id, username, email, password_hash }) => {
  try {
    const result = await pool.query(
      `INSERT INTO dev."Users_Info" (user_id, username, useremailid, password_hash, created_at)
             VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP) RETURNING *`,
      [id, username, email, password_hash]
    );
    return result.rows[0]; // Return the newly created user
  } catch (err) {
    console.error("Error creating user:", err);
    throw new Error("Error creating user");
  }
};

export const getUserByEmail = async (email) => {
  try {
    const result = await pool.query(
      `SELECT *
      FROM dev."Users_Info"
      WHERE useremailid = $1`,
      [email]
    );
    return result.rows[0]; // Return the user if found
  } catch (err) {
    console.error("Error finding user:", err);
    throw new Error("Error finding user");
  }
};

export const resetUserPassword = async (email, newPassword) => {
  const user = await getUserByEmail(email);
  if (!user) {
    throw new Error("User not found");
  }

  const hashedPassword = await bcrypt.hash(newPassword, 10);

  try {
    const result = await pool.query(
      `UPDATE dev."Users_Info" 
      SET password_hash = $1 
      WHERE useremailid = $2 
      RETURNING *`,
      [hashedPassword, email]
    );
    return result.rows[0]; // Return the updated user
  } catch (err) {
    console.error("Error updating password:", err);
    throw new Error("Error updating password");
  }
};

export const deleteUserById = async (id) => {
  try {
    const result = await pool.query(
      `DELETE FROM dev."Users_Info" 
      WHERE user_id = $1 RETURNING *`,
      [id]
    );
    if (result.rowCount === 0) {
      throw new Error("User not found");
    }
    return result.rows[0]; // Return the deleted user, if needed
  } catch (err) {
    console.error("Error deleting user:", err);
    throw new Error("Error deleting user");
  }
};

export const getUsers = async () => {
  try {
    const result = await pool.query(`SELECT * 
      FROM dev."Users_Info"`);
    return result.rows; // Return all users
  } catch (error) {
    console.error("Error fetching users:", error.message);
    throw new Error("Server Error");
  }
};
