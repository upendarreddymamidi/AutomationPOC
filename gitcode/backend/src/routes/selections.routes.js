import express from "express";
import {
  handleSelections,
  getData,
} from "../controllers/selections.controller.js";

const router = express.Router();

// Define the selections route (e.g., under /api/selections)
router.post("/", handleSelections);
router.get("/get/data", getData);

export default router;
