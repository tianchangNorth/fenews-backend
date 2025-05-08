import axios from 'axios';
import mongoose from 'mongoose';
import Article from '../models/article.js';

const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'; // 请替换为实际接口地址（如有不同）

const headers = {
  'Content-Type': 'application/json',
  Authorization: `Bearer ${DEEPSEEK_API_KEY}`,
};

async function callDeepSeek(content) {
  const body = {
    model: 'deepseek-chat', // 或 deepseek-coder, deepseek-v2 等，看你使用哪个模型
    messages: [
      {
        role: 'system',
        content: '你是一个擅长提炼技术文章的AI助手，请对以下内容进行评分、生成摘要并提取关键词。',
      },
      {
        role: 'user',
        content,
      },
    ],
    temperature: 0.7,
  };

  const res = await axios.post(DEEPSEEK_API_URL, body, { headers });
  return res.data.choices[0].message.content;
}

async function processArticles() {
  await mongoose.connect('mongodb://localhost:27017/fenews');
  const articles = await Article.find({ source: 'juejin' }).limit(3); // 限制条数调试用

  for (const article of articles) {
    const prompt = `标题：${article.title}\n简介：${article.brief}`;
    try {
      const result = await callDeepSeek(prompt);
      console.log(`🧠 AI处理结果 for "${article.title}":\n${result}\n`);
      
      // 可选择写回数据库（示例）
      // article.aiSummary = result;
      // await article.save();
    } catch (error) {
      console.error(`❌ 处理失败: ${article.title}`, error.message);
    }
  }

  process.exit();
}

processArticles();
