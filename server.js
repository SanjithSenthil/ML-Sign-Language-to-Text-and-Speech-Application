const express = require("express");
const path = require("path");
const { exec } = require("child_process");
const translatte = require("translatte");

const app = express();
const port = process.env.PORT || 3000;
    const langs = {
      "english": "en",
      "french": "fr",
      "chinese": "zh",
      "japanese": "ja",
      "spanish": "es"
    };

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, "public")));

// Define a route for the homepage
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.get("/run", (req, res) => {
  const scriptPath = `"${path.join(__dirname, "ASL.py")}"`;
  const lang = req.query.language;
  console.log(langs[lang]);
  exec(`python ${scriptPath} ${lang}`, async (error, stdout, stderr) => {
    if (error) {
        console.error(`Error executing x.py: ${error}`);
        res.status(500).send("Internal Server Error");
        return;
    }

    const lines = stdout.trim().split("\n");
    const lastLine = lines[lines.length - 1];
    console.log(lastLine);
    
    translatte(lastLine, { from: "en", to: langs[lang] })
        .then((translated) => {
            console.log(translated);

            // Redirect the user to the result page with translated text as a query parameter
            const translatedText = encodeURIComponent(translated.text);
            res.redirect(`/result?text=${translatedText}`);
        })
        .catch((err) => {
            console.error(err);
            res.status(500).send("Internal Server Error");
        });
});

});

// Define route for serving result.html
app.get('/result', (req, res) => {
  res.sendFile(path.join(__dirname, 'result.html'));
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
