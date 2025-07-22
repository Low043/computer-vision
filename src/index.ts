import ffmpeg from 'fluent-ffmpeg';
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';

dotenv.config();

const outputDir = path.join(__dirname, '..', 'output');

if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
}

ffmpeg(process.env.VIDEO_URL)
    .inputOptions('-rtsp_transport', 'tcp') // Usando protocolo tcp
    .outputOptions(['-vf', 'fps=1', '-q:v', '25']) // Salvando 1 frame p/s, qualidade 25 (2 a 31)

    // Manipuladores de eventos
    .on('start', (commandLine) => {
        console.log('🚀 Comando FFmpeg iniciado: ' + commandLine);
    })
    .on('error', (err) => {
        console.error('❌ Ocorreu um erro:', err.message);
    })
    .on('end', () => {
        console.log('✔️ Processamento finalizado.');
    })

    .save(path.join(outputDir, 'frame-%d.jpg')); //%d para número do frame
