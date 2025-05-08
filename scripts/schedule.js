// schedule.js
import cron from 'node-cron';
import { exec } from 'child_process';
import mongoose from 'mongoose';
import '../utils/loadEnv.js'

mongoose.connect(process.env.MONGO_URI).then(() => {
  console.log('✅ MongoDB 连接成功，启动定时任务...');
}).catch((err) => {
  console.error('❌ MongoDB 连接失败:', err);
});

cron.schedule('0 6 * * *', () => {
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

cron.schedule('0 8 * * *', () => {
  console.log(`🕒 ${new Date().toLocaleString()} 开始执行AI分析...`);
  exec('node scripts/processArticles.js', (error, stdout, stderr) => {
    if (error) {
      console.error(`❌ AI分析执行出错: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`⚠️ stderr: ${stderr}`);
      return;
    }
    console.log(`✅ AI分析执行输出:\n${stdout}`);
  });
});
