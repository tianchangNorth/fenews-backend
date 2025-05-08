import mongoose from 'mongoose';
import Article from '../models/article.js';
import ProcessedArticle from '../models/processedArticle.js';
import { chatWithAI } from '../utils/deepseek.js'; // 你封装的 AI 调用函数
import '../utils/loadEnv.js'

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
    const ratingText  = await chatWithAI(`文章标题：${article.title}\n\n文章简介: ${article.brief}`);
    let rating = parseFloat(ratingText.trim());

    if (isNaN(rating)) {
      rating = 5.0; // fallback
    }
    await ProcessedArticle.create({
      title: article.title,
      url: article.url,
      img: article.img,
      brief: article.brief,
      rating, // 添加 AI 评分
      source: article.source,
    });

    console.log(`✅ 分析完成: ${article.title}`);
  } catch (e) {
    console.error(`❌ 处理失败: ${article.title}`, e.message);
  }
}

await mongoose.disconnect();
