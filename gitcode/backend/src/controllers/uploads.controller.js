import multer from "multer";
import dotenv from "dotenv";
dotenv.config();

// Multer configuration
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadPath = process.env.UPLOADS_DIR || "default_upload_path";
    cb(null, uploadPath);
  },
  filename: (req, file, cb) => {
    try {
      const { env, user_id } = req.params;
      const timestamp = Date.now();

      const newFilename = `${env || "default_env"}_${
        user_id || "default_user"
      }_${timestamp}_${file.originalname}`;
      cb(null, newFilename);
    } catch (err) {
      console.error("Error generating filename:", err.message);
      cb(err);
    }
  },
});

// File filter to only accept .xlsx files
const fileFilter = (req, file, cb) => {
  const fileType = file.mimetype;
  if (
    fileType ===
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||
    file.originalname.endsWith(".xlsx")
  ) {
    cb(null, true);
  } else {
    cb(new Error("Only .xlsx files are allowed"), false);
  }
};

const upload = multer({ storage, fileFilter });

export const uploadFile = (req, res) => {
  upload.single("file")(req, res, (err) => {
    if (err) {
      console.error("Upload error:", err.message);
      return res.status(400).json({ error: err.message });
    }

    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded." });
    }

    console.log("Uploaded file:", req.file);
    res.status(200).json({
      message: "File successfully uploaded.",
      file: req.file.filename,
    });
  });
};
