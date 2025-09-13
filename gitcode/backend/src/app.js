import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import routes from "./routes/index.routes.js";
import pkg from "pg"; // Import Pool class

const { Pool } = pkg;
const app = express();

// Middleware
app.use(express.json());
app.use(cors());

// Load environment variables from the .env file
dotenv.config();

// Create a connection pool using the URI from the .env file
export const pool = new Pool({
  host: process.env.POSTGRES_HOST,
  database: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  port: 5432,
  ssl: { rejectUnauthorized: false },
});

// Optional: Adding an error handler for the pool
pool.on("error", (err) => {
  console.error("Unexpected error on idle client", err);
});

// Routes
app.use("/api", routes);

// Export
export default app;
