// schedule.js
import cron from 'node-cron';
import { exec } from 'child_process';
import mongoose from 'mongoose';
import dotenv from 'dotenv';

dotenv.config();

mongoose.connect(process.env.MONGO_URI).then(() => {
  console.log('✅ MongoDB 连接成功，启动定时任务...');
}).catch((err) => {
  console.error('❌ MongoDB 连接失败:', err);
});

// 每小时整点执行一次（你也可以改为每 10 分钟、每天等）
cron.schedule('0 8 * * *', () => {
  console.log(`🕒 ${new Date().toLocaleString()} 开始执行爬虫...`);
  exec('node scripts/fetchAndSaveArticles.js', (error, stdout, stderr) => {
    if (error) {
      console.error(`❌ 爬虫执行出错: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`⚠️ stderr: ${stderr}`);
      return;
    }
    console.log(`✅ 爬虫输出:\n${stdout}`);
  });
});
