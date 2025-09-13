import express from "express";
import userRoutes from "./user.routes.js";
import selectionRoutes from "./selections.routes.js";
import adminRoutes from "./admin.routes.js";
import uploadRoutes from "./uploads.routes.js";
import roboRoutes from "./robot.routes.js";

const router = express.Router();

// Use user routes
router.use("/users", userRoutes);
// Use selection routes
router.use("/selections", selectionRoutes);
// Use admin routes
router.use("/admin", adminRoutes);
// Use upload routes
router.use("/upload", uploadRoutes);
router.get("/users", userRoutes);
// Use robo routes
router.use("/robo", roboRoutes);

export default router;
