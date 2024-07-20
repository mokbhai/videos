const fs = require("fs").promises;
const { exec } = require("child_process");

async function processFile() {
  try {
    let data = await fs.readFile("data.txt", "utf8");
    let text = data.replace(/\n/g, " ").replace(/"/g, "'").replace(/\s+/g, " ");
    const voice = "en-CA-LiamNeural";
    const name = "126";

    exec(
      `edge-tts --voice ${voice} --text "${text}" --write-media ${name}.mp3 --write-subtitles ${name}.vtt`,
      (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        if (stderr) {
          console.log(`stderr: ${stderr}`);
        }
      }
    );
  } catch (err) {
    console.error(err);
  }
}

processFile();
