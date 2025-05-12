import express from 'express';
import processedArticle from '../models/processedArticle.js'; // 引入 Article 模型
import article from '../models/article.js';

const router = express.Router();

// 获取文章列表接口
router.get('/articles', async (req, res) => {
  const {category, limit} = req.query; // 获取查询参数
  
  try {
    // 你可以根据需求调整查询条件
    const articles = await article.find({category: category}).limit(limit).sort({ createdAt: -1 });
    res.json(articles); // 返回文章列表
  } catch (error) {
    console.error('Error fetching articles:', error);
    res.status(500).json({ error: 'Failed to fetch articles' });
  }
});

export default router;
