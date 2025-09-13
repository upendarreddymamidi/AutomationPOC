import globals from "globals";
import pluginJs from "@eslint/js";
import pluginReact from "eslint-plugin-react";

/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    languageOptions: {
      sourceType: "module", // 🔹 Change from "commonjs" to "module"
      ecmaVersion: "latest",
      globals: {
        ...globals.node, // Enable Node.js global variables
      },
    },
    rules: {
      "semi": ["error", "always"],
      "quotes": ["error", "double"],
    },
  },
  { languageOptions: { globals: globals.browser } },
  pluginJs.configs.recommended,
  pluginReact.configs.flat.recommended,
];
