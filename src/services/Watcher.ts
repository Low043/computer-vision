import ffmpeg from 'fluent-ffmpeg';
import { Writable } from 'stream';
import path from 'path';
import fs from 'fs';

class Watcher {
    private ffmpeg: ffmpeg.FfmpegCommand;
    private lastFrame: Buffer | null = null;
    private chunks: Buffer[] = [];

    constructor(videoURL: string) {
        this.ffmpeg = ffmpeg(videoURL)
            .inputOptions('-rtsp_transport', 'tcp')
            .outputOptions(['-vf', 'fps=10', '-q:v', '1'])
            .format('image2pipe');

            this.ffmpeg.pipe(new Writable({
                write: (chunk, encoding, callback) => {
                    this.chunks.push(chunk);
                    callback();
                },

                final: (callback) => {
                    this.lastFrame = Buffer.concat(this.chunks);
                    callback();
                }
            }), { end: true });
    }

    getLastFrame(): Buffer | null {
        return this.lastFrame;
    }
}

(async () => {
    const watcher = new Watcher('rtsp://admin:SEG101085$$a@10.0.0.157:554/cam/realmonitor?channel=1&subtype=1');
    
    setInterval(() => {
        const frame = watcher.getLastFrame();

        if (frame) {
            fs.writeFileSync(path.join(__dirname, 'lastFrame.png'), frame);
            console.log(frame);
        }
    }, 2000);
})();