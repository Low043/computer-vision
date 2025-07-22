import ffmpeg from 'fluent-ffmpeg';
import { Writable } from 'stream';
import Tesseract from 'tesseract.js';
import sharp from 'sharp';
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';

dotenv.config({ quiet: true });

async function getFrameBuffer(): Promise<Buffer> {
    return new Promise((resolve, reject) => {
        const dataChunks: Buffer[] = [];

        const memoryStream = new Writable({
            write(chunk, encoding, callback) {
                dataChunks.push(chunk);
                callback();
            },
        });

        const command = ffmpeg(process.env.VIDEO_URL)
            .inputOptions('-rtsp_transport', 'tcp')
            .outputOptions(['-vf', 'fps=1', '-frames:v', '1', '-q:v', '10', '-f', 'image2'])
            .on('error', (err) => {
                console.error(err.message);
                reject(err);
            })
            .on('end', () => {
                const frameBuffer = Buffer.concat(dataChunks);
                resolve(frameBuffer);
            });

        command.pipe(memoryStream);
    });
}

async function preprocessImage(imageBuffer: Buffer): Promise<Buffer> {
    const cropArea = {
        left: 350,
        top: 225,
        width: 210,
        height: 120,
    };

    // Recorta a imagem e aumenta o contraste
    return sharp(imageBuffer).extract(cropArea).normalise().toBuffer();
}

async function extractTextFromBuffer(imageBuffer: Buffer): Promise<string> {
    const worker = await Tesseract.createWorker('letsgodigital', Tesseract.OEM.TESSERACT_ONLY);
    worker.setParameters({
        tessedit_char_whitelist: '0123456789',
        tessedit_pageseg_mode: Tesseract.PSM.RAW_LINE
    });

    const { data: { text } } = await worker.recognize(imageBuffer);
    await worker.terminate();
    return text.trim();
}

(async () => {
    const outputDir = path.join(__dirname, '..', 'output');

    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    const imageBuffer = await getFrameBuffer();

    const processedBuffer = await preprocessImage(imageBuffer);
    fs.writeFileSync(path.join(outputDir, 'processed_image.png'), processedBuffer);

    const text = await extractTextFromBuffer(processedBuffer);

    console.log('Texto extraído:', text);
})();