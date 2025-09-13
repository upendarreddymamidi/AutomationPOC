import app from "./src/app.js";

const PORT = process.env.PORT || 4545;

app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
