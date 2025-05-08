// scripts/processArticles.js
import dotenv from 'dotenv';
import mongoose from 'mongoose';
import Article from '../models/article.js';
import ProcessedArticle from '../models/processedArticle.js';
import { chatWithAI } from '../utils/deepseek.js'; // 你封装的 AI 调用函数
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'

// 获取当前文件目录
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
dotenv.config({ path: resolve(__dirname, '../.env') })

await mongoose.connect(process.env.MONGO_URI);

console.log('🤖 开始处理 AI 分析任务...\n\n');

const articles = await Article.find(); // 可按需筛选未处理的

for (const article of articles) {
  const alreadyProcessed = await ProcessedArticle.findOne({ url: article.url });
  if (alreadyProcessed) {
    console.log(`⏭ 已处理: ${article.title}`);
    continue;
  }

  try {
    const tags = await chatWithAI(`请为以下内容提取3-5个关键词，返回数组格式：\n\n${article.title}\n\n${article.brief}`);

    await ProcessedArticle.create({
      title: article.title,
      url: article.url,
      img: article.img,
      brief: article.brief,
      tags: JSON.parse(tags),
      // categories: ['前端'], // 可选：你也可以用 AI 提取
      source: article.source,
    });

    console.log(`✅ 分析完成: ${article.title}`);
  } catch (e) {
    console.error(`❌ 处理失败: ${article.title}`, e.message);
  }
}

await mongoose.disconnect();
