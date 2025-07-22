import ffmpeg from 'fluent-ffmpeg';
import Tesseract from 'tesseract.js';
import sharp from 'sharp';
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';

dotenv.config();

const outputDir = path.join(__dirname, '..', 'output');

if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
}

async function processImage(imageBuffer: Buffer) {
    const cropArea = { left: 350, top: 195, width: 220, height: 92 };
    
    const result = await sharp(imageBuffer).extract(cropArea)
        .modulate({ brightness: 2, saturation: 20 })
        .normalise({ lower: 20, upper: 80 })
        .toBuffer();

    fs.writeFileSync(path.join(outputDir, 'processed.jpg'), result);

    return result;
}

async function getTextFromBuffer(imageBuffer: Buffer) {
    const result = await Tesseract.recognize(imageBuffer, 'ssd');
    return result.data.text;
}

(async () => {
    const imageBuffer = fs.readFileSync(path.join(outputDir, 'raw.jpg'));
    const processedImage = await processImage(imageBuffer);

    const text = await getTextFromBuffer(processedImage);
    console.log('Texto extraído:', text);
})();